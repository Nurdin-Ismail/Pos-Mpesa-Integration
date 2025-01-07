/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(PaymentScreen.prototype, {

    setup() {
        super.setup();
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.payment_methods_from_config
        if (this.currentOrder.selected_paymentline != undefined) {
            console.log(this.currentOrder.selected_paymentline)

        }
        this.pos = usePos();

    },

    async validateOrder(isForceValidate) {
        console.log(this.currentOrder.selected_paymentline)

        if (this.currentOrder.selected_paymentline.name == 'Mpesa') {
            const { confirmed, payload: phoneNumber } = await this.popup.add(NumberPopup, {
                title: _t('Enter Phone Number for MPesa'),
            });

            if (confirmed) {
                await this.notification.add(_t("Innitiating STK push!"), {
                    type: _t("info"),

                });
                try {
                    // Step 1: Get the access token first
                    const accessTokenResponse = await this.rpc("/mpesa/access_token", {
                        params: {}
                    });

                    // Check if access_token was retrieved successfully
                    if (accessTokenResponse && accessTokenResponse.access_token) {
                        const access_token = accessTokenResponse.access_token;
                        console.log(access_token)
                        const amount = this.currentOrder.selected_paymentline.amount
                        const thisOrder = this.pos.get_order();

                        console.log(thisOrder)


                        // Step 2: Initiate the MPesa STK Push with the access token
                        const stkPushResponse = await this.rpc("/mpesa/stk_push", {


                            access_token,
                            phoneNumber,
                            amount

                        });



                        // await this.rpc({
                        //     model: 'pos.mpesa',
                        //     method: 'mpesa_stk_push',
                        //     kwargs: [{
                        //         access_token,
                        //         phoneNumber,
                        //         amount
                        //     }]
                        // });





                        // Handle the response from the STK push
                        if (stkPushResponse && !stkPushResponse.errorCode) {

                            await this.notification.add(_t("Insert number on the incoming STK push!"), {
                                type: _t("info"),

                            });





                            console.log(stkPushResponse)

                            const checkout_request_id = stkPushResponse.CheckoutRequestID
                            const thisOrder = this.pos.get_order().name;

                            const queryResponse = await this.rpc("/mpesa/query", {
                                checkout_request_id,
                                thisOrder,
                            });

                            if (queryResponse && !queryResponse.error) {
                                console.log(queryResponse)
                                if (queryResponse.ResultCode == "0") {
                                    await this.notification.add(_t("MPesa payment was successful!"), {
                                        type: _t("success"),
                                        title: _t("Success"),

                                    });
                                    return super.validateOrder(isForceValidate);


                                } else if (queryResponse.ResultCode != "0") {
                                    await this.notification.add(_t(queryResponse.ResultDesc), {
                                        type: _t("warning"),
                                        title: _t('Timeout. Retry')


                                    });

                                }
                            }





                        } else {
                            console.log(stkPushResponse)

                            // alert('MPesa payment failed. Please try again.');
                            await this.notification.add(_t(stkPushResponse.errorMessage), {
                                type: _t("danger"),
                                title: _t('MPesa payment failed. Please try again.')

                            });
                        }
                    } else {
                        // Handle access token retrieval failure
                        console.log(accessTokenResponse)
                    }
                } catch (error) {
                    console.error('Error:', error);
                    await this.notification.add(_t('An error occurred during MPesa payment.'), {
                        type: _t("danger"),

                    });

                }
            }
        } else {
            return super.validateOrder(isForceValidate);

        }


        // Continue with the normal order validation
        // return super.validateOrder(isForceValidate);
    },

});
