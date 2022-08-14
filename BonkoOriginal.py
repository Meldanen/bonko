import sys

from discord import Webhook, RequestsWebhookAdapter


def bonkero():
    url_general = "https://discord.com/api/webhooks/840906215759937556/vh5Gien4rLmCabJkPfheyKwG4fu5LTB_EIWB40XM1UIOqx8aSV7mIVLVuL4peF3Myzdw"
    url_nutrition = "https://discord.com/api/webhooks/840936624673259540/Y4CSVUqsU34Qolh-9HfKB7ti9OqwCfXU9SrrIirJkdFTHBKwlXVvldllzicIYGXMSY7p"
    url_jobs = "https://discord.com/api/webhooks/841264882183307294/dCBRzRAV6Km7-L4kR5rcSm7i1LyamQDK680WmMsPOc-GHCzmUdAXOzXx-DW-WX-J2UUM"
    url_stupids = "https://discord.com/api/webhooks/841649036607356949/sFTnoJENIiVSUmWG1DaBT0tVbFHsFFwN6JQogWfevwHCAft8rd2b_9CsGrop9oo5z5UJ"
    bonk = "<:bonk:755409585841504358>"
    giannakis = "<@!294577564603645952>"
    channel = sys.argv[1];

    url = None

    if channel == "nutrition":
        url = url_nutrition
    elif channel == "general":
        url = url_general
    elif channel == "jobs":
        url = url_jobs
    elif channel == "stupids":
        url = url_stupids

    if url:
        webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
        webhook.send("bonk giannaki")
        webhook.send(bonk + " " + giannakis)
        webhook.send(bonk)


if __name__ == '__main__':
    bonkero()
