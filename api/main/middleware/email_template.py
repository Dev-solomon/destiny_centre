def order_template(order):
    return f"""
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #e8ebe9; padding-top: 20px;">
    <tr>
        <td align="center">
            <div style="width: 100%; max-width: 650px; margin: 0 auto;">
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width: 650px; margin: 0 auto;">
                    <tbody>
                        <tr>
                            <td>
                                <table width="100%" bgcolor="#ffffff" cellpadding="0" cellspacing="0" border="0" style="margin: 0 auto; background: #ffffff;">
                                    <tbody>
                                        <tr>
                                            <td style="padding:70px 0px; background-color: #e9fff2">
                                                <div style="text-align: center;">
                                                    <a href="{order['url']}" target="_blank" style="display: inline-block;">
                                                        <img style="width: 100%; height: 70px;" src="https://res.cloudinary.com/dns8ckviy/image/upload/v1718299320/lizie_ctniwa.png" alt="">
                                                    </a>
                                                </div>
                                                <div style="color: #000000; font-size: 15px; font-family: Verdana, sans-serif; text-align: center;margin: 30px 0;">
                                                    Thank you for shopping with us. Here are the details of your order.
                                                </div>
                                                <div style="text-align: center;">
                                                    <button style="background-color: #09d4fc; width:27%; padding: 14px 0px; border: none; border-radius: 100px; font-size: 15px; font-family: Verdana, sans-serif;">
                                                        <a href="{order['orderUrl']}" target="_blank" style="color: #ffffff; text-decoration: none;">
                                                            View Order
                                                        </a>
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border: 2px solid #f1f0f0;">
                                                    <tbody>
                                                        <tr>
                                                            <td width="600" style="padding-top: 70px; padding-bottom: 40px; padding-left: 70px; padding-right: 70px;">
                                                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                                    <tbody>
                                                                        {''.join(f"""
                                                                            <tr>
                                                                                <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                                                                                    <div style="margin-bottom: 15px; display:flex; align-items:center;">
                                                                                        <img src="{item['image']}" alt="" style="width: 60px; height: 60px; margin-top:10px; margin-right:10px;object-fit: cover;">
                                                                                        <div>
                                                                                            <a href="{order['url']}/card/{item['product']}" style="color: #0b32a6;font-size:15px;margin-bottom:2px">{item['name']}</a>
                                                                                            <p style="font-size:15px;margin-bottom:2px">Size : {item['size']}</p>
                                                                                            <p style="font-size:15px">Color : {item['color']}</p>
                                                                                        </div>
                                                                                    </div>
                                                                                    <div style="border-bottom: 1px solid #edecec;"></div>
                                                                                </td>
                                                                            </tr>
                                                                        """ for item in order["products"])}
                                                                        <tr>
                                                                            <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                                                                                <div style="padding:20px 0">
                                                                                    <label style="font-size:15px">Subtotal</label>
                                                                                    <div style="font-weight: 600;font-size:13px;float:right">€{float(order["subTotal"]):,.2f}</div>
                                                                                </div>
                                                                                <div style="border-bottom:1px solid #edecec;"></div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                                                                                <div style="padding:20px 0">
                                                                                    <label style="font-size:15px">Shipping cost</label>
                                                                                    <div style="font-weight: 600;font-size:13px;float:right">€{float(order["shippingCost"]):,.2f}</div>
                                                                                </div>
                                                                                <div style="border-bottom:1px solid #edecec;"></div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                                                                                <div style="padding:20px 0">
                                                                                    <label style="font-size:15px">Tax</label>
                                                                                    <div style="font-weight: 600;font-size:13px;float:right">€{float(order["taxPrice"]):,.2f}</div>
                                                                                </div>
                                                                                <div style="border-bottom:1px solid #edecec;"></div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td style="font-family: Verdana, sans-serif; color: #000000; text-align: left;">
                                                                                <div style="padding:20px 0">
                                                                                    <label style="font-size:15px">Total</label>
                                                                                    <div style="font-weight: 600;font-size:13px;float:right">€{float(order["totalPrice"]):,.2f}</div>
                                                                                </div>
                                                                                <div style="border-bottom:1px solid #edecec;"></div>
                                                                            </td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td height="50"></td>
                                                                        </tr>
                                                                        <tr>
                                                                            <td>
                                                                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="text-align: center;">
                                                                                                <a href="https://www.instagram.com/liziestyle_ecommerce/" target="_blank" style="display: inline-block; margin-left: 3px; margin-right: 3px;">
                                                                                                    <img src="http://stansafaris.com/wp-content/plugins/cf7-email-add-on/admin/assets/images/instagram-icon.png">
                                                                                                </a>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </td>
                                                                        </tr>
                                                                    </tbody>
                                                                </table>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </td>
    </tr>
    <tr>
        <td>
            <div style="width: 100%; max-width: 620px; margin: 0 auto;">
                <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="font-family: Verdana, sans-serif; font-weight: normal; font-size: 14px; line-height: 24px; color: black; text-align: left; padding-bottom: 30px; padding-top: 15px;">
                            Copyright © 2023 <a href="{order['url']}" target="_blank" style="text-decoration: none; color: #09d4fc">{order["siteName"]}</a>
                        </td>
                        <td style="font-family: Verdana, sans-serif; font-weight: normal; font-size: 14px; line-height: 24px; color: black; text-align: right; padding-bottom: 30px; padding-top: 15px;">
                            Powered by <a href="#" target="_blank" style="text-decoration: none; color: #09d4fc;">{order["siteName"]} Company</a>
                        </td>
                    </tr>
                </table>
            </div>
        </td>
    </tr>
    </table>
    """
    


def payment_template(notice):
    return f"""
    <style media="all" type="text/css">
    @media all {{
      .btn-primary table td:hover {{
        background-color: #ec0867 !important;
      }}

      .btn-primary a:hover {{
        background-color: #ec0867 !important;
        border-color: #ec0867 !important;
      }}
        .styled-button {{
        display: inline-block;
        padding: 10px 20px;
        background-color: #09d4fc; /* Green */
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }}

    .styled-button:hover {{
        background-color: #45a049; /* Darker green */
    }}
    }}
    @media only screen and (max-width: 640px) {{
      .main p,
    .main td,
    .main span {{
        font-size: 16px !important;
      }}

      .wrapper {{
        padding: 8px !important;
      }}

      .content {{
        padding: 0 !important;
      }}

      .container {{
        padding: 0 !important;
        padding-top: 8px !important;
        width: 100% !important;
      }}

      .main {{
        border-left-width: 0 !important;
        border-radius: 0 !important;
        border-right-width: 0 !important;
      }}

      .btn table {{
        max-width: 100% !important;
        width: 100% !important;
      }}

      .btn a {{
        font-size: 16px !important;
        max-width: 100% !important;
        width: 100% !important;
      }}
        .styled-button {{
        display: inline-block;
        padding: 10px 20px;
        background-color:  #09d4fc; /* Green */
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }}

    .styled-button:hover {{
        background-color: #45a049; /* Darker green */
    }}
    }}
    @media all {{
      .ExternalClass {{
        width: 100%;
      }}

      .ExternalClass,
    .ExternalClass p,
    .ExternalClass span,
    .ExternalClass font,
    .ExternalClass td,
    .ExternalClass div {{
        line-height: 100%;
      }}

      .apple-link a {{
        color: inherit !important;
        font-family: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        text-decoration: none !important;
      }}

      #MessageViewBody a {{
        color: inherit;
        text-decoration: none;
        font-size: inherit;
        font-family: inherit;
        font-weight: inherit;
        line-height: inherit;
      }}
        .styled-button {{
        display: inline-block;
        padding: 10px 20px;
        background-color:  #09d4fc; /* Green */
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }}

    .styled-button:hover {{
        background-color: #45a049; /* Darker green */
    }}
    }}
    </style>
    <table border="0" cellpadding="0" cellspacing="0" class="body" style="border-collapse: separate;  width: 100%;" width="100%">
        <tr>
          <td style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top;" valign="top">&nbsp;</td>
          <td class="container" style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top; max-width: 600px; padding: 0; padding-top: 24px; width: 600px; margin: 0 auto;" width="600" valign="top">
            <div class="content" style="box-sizing: border-box; display: block; margin: 0 auto; max-width: 600px; padding: 0;">

             <table role="presentation" border="0" cellpadding="0" cellspacing="0" class="main" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; background: #ffffff; border: 1px solid #eaebed; border-radius: 16px; width: 100%;" width="100%">

                <!-- START MAIN CONTENT AREA -->
                <tr>
                  <td class="wrapper" style="font-family: Helvetica, sans-serif; font-size: 16px; vertical-align: top; box-sizing: border-box; padding: 24px;" valign="top">
                    {f"""
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px; text-align: center">New Transaction Update!</p>
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px;">Our System Just Made a recent payment for a customer's order to CjDropsipping services. </p>
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px;">Here are the details: </p>
                      <ul>
                          <li>API Code: {notice['code']}</li>
                          <li>Order ID: {notice['orderId']}</li>
                          <li>API Message: {notice['message']}</li>
                        </ul>
                    """ if notice['purpose'] == 'OPS' else f"""
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px; text-align: center">Urgent Notice!!!</p>
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px;"> A payment process was initiated by our system for a customer's order and rendered Invalid. </p>
                     <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin: 0; margin-bottom: 16px;">Here are the details: </p>
                      <ul>
                        <li>Account Balance: ${notice['accBalance']}</li>
                        <li>Order ID: {notice['orderId']}</li>
                        <li>Total Order Amount: ${notice['totalOrderAmount']}</li>
                      </ul>
                       <div style="text-align: center;">
                         <button style="background-color: #09d4fc; width:27%; padding: 15px 0px; border: none; border-radius: 10px; font-size: 15px; font-family: Verdana, sans-serif;">
                          <a href="{notice['url']}" target="_blank" style="color: #ffffff; text-decoration: none;">
                            Pay Now
                          </a>
                        </button>
                    """}
                     <br style="width: 85%"/>
                    <p style="font-family: Helvetica, sans-serif; font-size: 16px; font-weight: normal; margin-top: 10px; margin-bottom: 16px; color:#09d4fc ">Powered by Liziestyle Ecommerce</p>
                  </td>
                </tr>

                <!-- END MAIN CONTENT AREA -->
                </table>
    """

    
    

