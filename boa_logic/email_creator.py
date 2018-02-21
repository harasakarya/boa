

class EmailCreator():

    def return_contents(self, filename):
        with open(filename, 'r') as myfile:
            return myfile.read().replace('\n', '')

    def make_email(self, coins):

        html = "<tr>"
        coin_counter = 0
        for coin in coins:

            #email above and below
            email_body = '''<!-- Column : BEGIN -->
                        <td width="33.33%" class="stack-column-center">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0">
                                <tr>
                                    <td style="padding: 10px; text-align: center">
                                        <img src="https://files.coinmarketcap.com/static/img/coins/128x128/''' + coin.get_name() +'''.png" width="170" height="170" alt="alt_text" border="0" class="fluid" style="height: auto; background: #dddddd; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                                    </td>
                                </tr>
                                <tr>
                                    <td style="font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; padding: 0 10px 10px; text-align: left;" class="center-on-narrow">
                                        '''

            email_body2 = '''
                                    </td>
                                </tr>
                            </table>
                        </td>
                        <!-- Column : END -->'''

            #coin analysis

            tldr_val = coin.get_prediction_plus(
                coin.get_most_recent_pattern()) if coin.get_stationarity() else coin.get_stationarity_as_string()
            if coin_counter % 3 == 0:
                html += "</tr><tr>"
            html += email_body + '''
                            <h2> ''' + coin.get_name() + '''</h2>

                                <h4>
                                    <b> TL;DR: ''' + tldr_val + '''</b>
                                </h4>
                                <ul>
                                    <li><b>''' + coin.get_stationarity_as_string() + '''</b>, Chi-Square sigma: ''' + coin.get_stat_sigma() + ''', 
                                    Chi-Square critical value: ''' + coin.get_stat_critical_value() + '''</li>
                                    <li><b>''' + coin.get_randomness_as_string() + '''ly</b> distributed, Chi-Square sigma: 
                                        ''' + coin.get_rand_sigma() + '''Chi-Square critical value: ''' + coin.get_rand_critical_value() + '''
                                    <li><b>''' + coin.get_independence_as_string() + '''</b>, Chi-Square sigma:  ''' + coin.get_ind_sigma() + '''
                                    Chi-Square critical value: ''' + coin.get_ind_critical_value() + '''</li>
                                </ul>

                                <!--

                                <p>After analysing the price history, BOA concluded that there is a <b>''' + '%.2f' % coin.get_odds_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go up, and a <b>''' + '%.2f' % coin.get_odds_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>
                                chance price will go down. The average magnitude of the up move is <b>''' + '%.2f' % coin.get_magnitude_of_increase(
                coin.get_most_recent_pattern()) + '''%</b>
                                and the average magnitude of the down move is <b>''' + '%.2f' % coin.get_magnitude_of_decrease(
                coin.get_most_recent_pattern()) + '''%</b>.
                                Today, you should <b>''' + coin.get_prediction_plus(coin.get_most_recent_pattern()) + '''</b>.
                                </p>
                                <br/> -->
                ''' + email_body2
            coin_counter += 1

        return self.email_a + html + "<tr>" + self.email_b

    def __init__(self):

        self.email_a = '''
        <!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title>BOA Report</title>
    <style>

        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
        }

        /* What it does: Stops email clients resizing small text. */
        * {
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {
            margin: 0 !important;
        }

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }

        /* What it does: Fixes webkit padding issue. Fix for Yahoo mail table alignment bug. Applies table-layout to the first 2 tables then removes for anything nested deeper. */
        table {
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }
        table table table {
            table-layout: auto;
        }

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {
            -ms-interpolation-mode:bicubic;
        }

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .x-gmail-data-detectors,    /* Gmail */
        .x-gmail-data-detectors *,
        .aBn {
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }

        /* What it does: Prevents Gmail from displaying an download button on large, non-linked images. */
        .a6S {
           display: none !important;
           opacity: 0.01 !important;
       }
       /* If the above doesn't work, add a .g-img class to any image in question. */
       img.g-img + div {
           display: none !important;
       }

       /* What it does: Prevents underlining the button text in Windows 10 */
        .button-link {
            text-decoration: none !important;
        }

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */
        /* Thanks to Eric Lepetit (@ericlepetitsf) for help troubleshooting */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) { /* iPhone 6 and 6+ */
            .email-container {
                min-width: 375px !important;
            }
        }

	    @media screen and (max-width: 480px) {
	        /* What it does: Forces Gmail app to display email full width */
	        div > u ~ div .gmail {
		        min-width: 100vw;
	        }
		}

    </style>
    <!-- CSS Reset : END -->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

        /* What it does: Hover styles for buttons */
        .button-td,
        .button-a {
            transition: all 100ms ease-in;
        }
        .button-td:hover,
        .button-a:hover {
            background: #555555 !important;
            border-color: #555555 !important;
        }

        /* Media Queries */
        @media screen and (max-width: 600px) {

            .email-container {
                width: 100% !important;
                margin: auto !important;
            }

            /* What it does: Forces elements to resize to the full width of their container. Useful for resizing images beyond their max-width. */
            .fluid {
                max-width: 100% !important;
                height: auto !important;
                margin-left: auto !important;
                margin-right: auto !important;
            }

            /* What it does: Forces table cells into full-width rows. */
            .stack-column,
            .stack-column-center {
                display: block !important;
                width: 100% !important;
                max-width: 100% !important;
                direction: ltr !important;
            }
            /* And center justify these ones. */
            .stack-column-center {
                text-align: center !important;
            }

            /* What it does: Generic utility class for centering. Useful for images, buttons, and nested tables. */
            .center-on-narrow {
                text-align: center !important;
                display: block !important;
                margin-left: auto !important;
                margin-right: auto !important;
                float: none !important;
            }
            table.center-on-narrow {
                display: inline-block !important;
            }

            /* What it does: Adjust typography on small screens to improve readability */
            .email-container p {
                font-size: 17px !important;
            }
        }

    </style>
    <!-- Progressive Enhancements : END -->

    <!-- What it does: Makes background images in 72ppi Outlook render at correct size. -->
    <!--[if gte mso 9]>
    <xml>
        <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
    </xml>
    <![endif]-->

</head>
<body width="100%" bgcolor="#222222" style="margin: 0; mso-line-height-rule: exactly;">
    <center style="width: 100%; background: #222222; text-align: left;">

        <!-- Email Body : BEGIN -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="600" style="margin: auto;" class="email-container">

            <!-- Hero Image, Flush : BEGIN -->
            <tr>
                <td bgcolor="#ffffff" align="center">
                    <img src="images/bitcoin.jpeg" width="600" height="" alt="alt_text" border="0" align="center" style="width: 100%; max-width: 600px; height: auto; background: #dddddd; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; margin: auto;" class="g-img">
                </td>
            </tr>
            <!-- Hero Image, Flush : END -->

            <!-- 1 Column Text + Button : BEGIN -->
            <tr>
                <td bgcolor="#ffffff" style="padding: 40px 40px 20px; text-align: center;">
                    <h1 style="margin: 0; font-family: sans-serif; font-size: 24px; line-height: 125%; color: #333333; font-weight: normal;">BOA Report
                        <script> document.write(new Date().toLocaleDateString()); </script></h1>
                </td>
            </tr>
            <tr>
                <td bgcolor="#ffffff" style="padding: 0 40px 40px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555; text-align: center;">
                    <p style="margin: 0;">Here's BOA's analysis for today. Remember to use the analysis in conjunction with your own trading or investing strategy. For a breakdown of how to read the email, watch <a href="https://www.youtube.com/watch?v=7o-mrb3pKQ0" target="">this</a> 13 minute video.</p>
                </td>
            </tr>
            <!-- 1 Column Text + Button : END -->

            <!-- Background Image with Text : BEGIN -->
            <tr>
                <!-- Bulletproof Background Images c/o https://backgrounds.cm -->
                <td bgcolor="#222222" valign="middle" style="text-align: center; background-position: center center !important; background-size: cover !important;">
                <div>
                    <table role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td valign="middle" style="text-align: center; padding: 40px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #ffffff;">
                                <p style="margin: 0;">To learn about stationarity, randomness, and independence in cryptocurrencies, watch <a href="https://www.youtube.com/watch?v=jar7xRk-Lb0" target="">this</a> 14 minute video.</p>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
        <!-- Background Image with Text : END -->

        <!-- 3 Even Columns : BEGIN -->
        <tr>
            <td bgcolor="#ffffff" align="center" valign="top" style="padding: 10px;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
        '''

        self.email_b = '''
        </table>
            </td>
        </tr>

        <!-- 3 Even Columns : END -->

        <!-- Clear Spacer : BEGIN -->
        <tr>
            <td aria-hidden="true" height="40" style="font-size: 0; line-height: 0;">
                &nbsp;
            </td>
        </tr>
        <!-- Clear Spacer : END -->

        <!-- 1 Column Text : BEGIN -->
        <tr>
            <td bgcolor="#ffffff">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="padding: 40px; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #555555;">
                            We hope BOA is useful to you in your cryptocurrency trading and investing. If you enjoy the email, consider forwarding it to a friend, who can get his or her own free daily email at <a href="cryptoboa.io"> cryptoboa.io</a>!
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <!-- 1 Column Text : END -->

    </table>
    <!-- Email Body : END -->

    <!-- Email Footer : BEGIN -->
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" width="100%" style="max-width: 680px; font-family: sans-serif; color: #888888; font-size: 12px; line-height: 140%;">
        <!--<tr>
            <td style="padding: 40px 10px; width: 100%; font-family: sans-serif; font-size: 12px; line-height: 140%; text-align: center; color: #888888;" class="x-gmail-data-detectors">
                <webversion style="color: #cccccc; text-decoration: underline; font-weight: bold;">View as a Web Page</webversion>
                <br><br>
                Company Name<br>123 Fake Street, SpringField, OR, 97477 US<br>(123) 456-7890
                <br><br>
                <unsubscribe style="color: #888888; text-decoration: underline;">unsubscribe</unsubscribe>
            </td>
        </tr>-->
    </table>
    <!-- Email Footer : END -->

    <!-- Full Bleed Background Section : BEGIN -->
    <table role="presentation" bgcolor="#554a8d" cellspacing="0" cellpadding="0" border="0" align="center" width="100%">
        <tr>
            <td valign="top" align="center">
                <div style="max-width: 600px; margin: auto;" class="email-container">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                        <tr>
                            <td style="padding: 40px; text-align: left; font-family: sans-serif; font-size: 15px; line-height: 140%; color: #ffffff;">
                                <p style="margin: 0;">Disclaimer: The information provided here and in accompanying material is for informational purposes only. It should not be considered legal or financial advice. You should consult with an attorney, financial advisor or other professional to determine what may be best for your individual needs. I do not make any guarantee or other promise as to any results that may be obtained from using this content. No one should make any investment decision without first consulting his or her own financial advisor and conducting his or her own research and due diligence.</p>
                            </td>
                        </tr>
                    </table>
                </div>
            </td>
        </tr>
    </table>
    <!-- Full Bleed Background Section : END -->

    </center>
</body>
</html>

        '''