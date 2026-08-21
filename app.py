from flask import Flask, request, render_template_string, make_response
from ask_ai import ask_ai
import re
import html


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# ============================================================
# COMPANY DETAILS
# ============================================================

COMPANY_NAME = "TechNova Solutions Pvt. Ltd."

PHONE = "+91 1800 123 4567"
PHONE_LINK = "tel:+9118001234567"

EMAIL = "support@technova.com"
EMAIL_LINK = "mailto:support@technova.com"

WEBSITE = "https://www.technova.com"
WORKING_HOURS = "Monday - Saturday, 9:00 AM - 6:00 PM"


# ============================================================
# MEMORY
# ============================================================

memory = []

MAX_INPUT_LENGTH = 2000


# ============================================================
# INPUT GUARDRAIL
# ============================================================

def input_guardrail(query):

    if not isinstance(query, str):
        return False, "Input must be text."

    query = query.strip()

    if not query:
        return False, "Please enter your support query."

    if len(query) > MAX_INPUT_LENGTH:
        return False, "Query is too long. Maximum 2000 characters allowed."

    return True, query


# ============================================================
# CLEAN AI RESPONSE
# ============================================================

def clean_response(text):

    if not text:
        return ""

    text = str(text)

    # Remove carriage returns
    text = text.replace("\r", "")

    # Remove markdown headings
    text = re.sub(
        r'^\s*#{1,6}\s*',
        '',
        text,
        flags=re.MULTILINE
    )

    # Remove markdown bold
    text = text.replace("**", "")

    # Remove markdown italic
    text = text.replace("__", "")

    # Remove markdown code markers
    text = text.replace("```", "")

    # Remove excessive blank lines
    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines).strip()


# ============================================================
# ROUTER AGENT
# ============================================================

def router_agent(query):

    role = """
You are the Customer Support Router Agent for TechNova Solutions Pvt. Ltd.

Classify the customer query into exactly ONE category:

BILLING
TECHNICAL
REFUND
GENERAL

BILLING:
Payment, invoice, subscription, charge or billing issues.

TECHNICAL:
Login, application errors, bugs or technical problems.

REFUND:
Refund, cancellation or money-back requests.

GENERAL:
General questions that do not belong to the above categories.

IMPORTANT:
Return ONLY the category name.
Do not return explanations.
"""

    result = ask_ai(role, query)

    result = result.strip().upper()

    if result == "BILLING":
        return "Billing Agent"

    if result == "TECHNICAL":
        return "Technical Agent"

    if result == "REFUND":
        return "Refund Agent"

    return "General Agent"


# ============================================================
# BILLING AGENT
# ============================================================

def billing_agent(query):

    role = f"""
You are the Billing Support Agent for {COMPANY_NAME}.

Help customers with:

- Payments
- Invoices
- Subscriptions
- Duplicate charges
- Billing problems

Give clear and professional answers.

Support details:

Helpline: {PHONE}
Email: {EMAIL}
Working Hours: {WORKING_HOURS}

Do not invent company policies.
Do not invent contact information.
"""

    return clean_response(
        ask_ai(role, query)
    )


# ============================================================
# TECHNICAL AGENT
# ============================================================

def technical_agent(query):

    role = f"""
You are the Technical Support Agent for {COMPANY_NAME}.

Help customers with:

- Login problems
- Password problems
- Application errors
- Bugs
- Technical issues

Give simple step-by-step solutions.

Support details:

Helpline: {PHONE}
Email: {EMAIL}
Working Hours: {WORKING_HOURS}

Do not invent company policies.
Do not invent contact information.
"""

    return clean_response(
        ask_ai(role, query)
    )


# ============================================================
# REFUND AGENT
# ============================================================

def refund_agent(query):

    role = f"""
You are the Refund Support Agent for {COMPANY_NAME}.

Help customers with:

- Refund requests
- Cancellation requests
- Money-back requests
- Payment reversals

Be polite and professional.

Support details:

Helpline: {PHONE}
Email: {EMAIL}
Working Hours: {WORKING_HOURS}

Do not invent company policies.
Do not invent contact information.
"""

    return clean_response(
        ask_ai(role, query)
    )


# ============================================================
# GENERAL AGENT
# ============================================================

def general_agent(query):

    role = f"""
You are the General Customer Support Agent for {COMPANY_NAME}.

Answer customer questions clearly,
professionally and politely.

Support details:

Helpline: {PHONE}
Email: {EMAIL}
Working Hours: {WORKING_HOURS}

Do not invent company policies.
Do not invent contact information.
"""

    return clean_response(
        ask_ai(role, query)
    )


# ============================================================
# AGENT REGISTRY
# ============================================================

AGENTS = {

    "Billing Agent": billing_agent,

    "Technical Agent": technical_agent,

    "Refund Agent": refund_agent,

    "General Agent": general_agent

}


# ============================================================
# MAIN FRONTEND
# ============================================================

HTML = """

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>TechNova Customer Support</title>


<style>

/* ============================================================
   RESET
   ============================================================ */

* {
    box-sizing: border-box;
}


/* ============================================================
   BODY
   ============================================================ */

body {

    margin: 0;

    font-family: Arial, Helvetica, sans-serif;

    background: #f1f5f9;

    color: #1e293b;

}


/* ============================================================
   NAVBAR
   ============================================================ */

.navbar {

    background: #0f172a;

    color: white;

    padding: 18px 7%;

    display: flex;

    justify-content: space-between;

    align-items: center;

}


.logo {

    font-size: 25px;

    font-weight: bold;

    color: #38bdf8;

}


.nav-text {

    color: #cbd5e1;

    font-size: 14px;

}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    background: linear-gradient(
        135deg,
        #0f172a,
        #1d4ed8
    );

    color: white;

    padding: 70px 7%;

}


.company-label {

    display: inline-block;

    padding: 8px 16px;

    border-radius: 20px;

    background: #38bdf8;

    color: #082f49;

    font-weight: bold;

}


.hero h1 {

    font-size: 42px;

    margin: 20px 0 10px 0;

}


.hero p {

    max-width: 750px;

    font-size: 18px;

    line-height: 1.7;

    color: #dbeafe;

}


/* ============================================================
   CONTAINER
   ============================================================ */

.container {

    width: 86%;

    max-width: 1100px;

    margin: -35px auto 40px auto;

}


/* ============================================================
   CARD
   ============================================================ */

.card {

    background: white;

    padding: 30px;

    border-radius: 18px;

    margin-bottom: 25px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.10);

}


.card h2 {

    margin-top: 0;

    color: #0f172a;

}


/* ============================================================
   AGENTS
   ============================================================ */

.agents {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(200px, 1fr));

    gap: 18px;

}


.agent {

    padding: 25px;

    border-radius: 15px;

    color: white;

    text-align: center;

}


.agent-icon {

    font-size: 35px;

    margin-bottom: 10px;

}


.agent h3 {

    margin: 5px;

}


.agent p {

    font-size: 14px;

    line-height: 1.5;

}


.billing {

    background: #2563eb;

}


.technical {

    background: #ea580c;

}


.refund {

    background: #7c3aed;

}


.general {

    background: #16a34a;

}


/* ============================================================
   TEXTAREA
   ============================================================ */

textarea {

    width: 100%;

    height: 150px;

    padding: 16px;

    border: 1px solid #cbd5e1;

    border-radius: 12px;

    font-size: 16px;

    resize: vertical;

    font-family: Arial, sans-serif;

}


textarea:focus {

    outline: none;

    border: 2px solid #2563eb;

}


/* ============================================================
   BUTTON
   ============================================================ */

button {

    margin-top: 15px;

    padding: 14px 28px;

    background: #2563eb;

    color: white;

    border: none;

    border-radius: 10px;

    font-size: 16px;

    font-weight: bold;

    cursor: pointer;

}


button:hover {

    background: #1d4ed8;

}


/* ============================================================
   ERROR
   ============================================================ */

.error {

    margin-top: 20px;

    padding: 16px;

    border-radius: 10px;

    background: #fee2e2;

    color: #991b1b;

    border-left: 5px solid #dc2626;

}


/* ============================================================
   SELECTED AGENT
   ============================================================ */

.selected-agent {

    margin-top: 20px;

    padding: 18px;

    background: #dcfce7;

    border-left: 5px solid #16a34a;

    border-radius: 10px;

}


.selected-agent h3 {

    margin: 0 0 8px 0;

    color: #166534;

}


.agent-name {

    font-size: 20px;

    font-weight: bold;

    color: #15803d;

}


/* ============================================================
   AI RESPONSE
   ============================================================ */

.response {

    margin-top: 20px;

    padding: 20px;

    background: #f8fafc;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    line-height: 1.6;

}


.response h3 {

    color: #1d4ed8;

    margin: 0 0 12px 0;

}


.ai-text {

    margin: 0;

    white-space: pre-line;

    line-height: 1.7;

}


/* ============================================================
   SUPPORT LINKS
   ============================================================ */

.support-link {

    display: inline-block;

    padding: 12px 18px;

    color: white;

    text-decoration: none;

    border-radius: 8px;

    font-weight: bold;

    margin: 5px;

}


.call-link {

    background: #2563eb;

}


.call-link:hover {

    background: #1d4ed8;

}


.email-link {

    background: #7c3aed;

}


.email-link:hover {

    background: #6d28d9;

}


.website-link {

    background: #16a34a;

}


.website-link:hover {

    background: #15803d;

}


/* ============================================================
   CONTACT GRID
   ============================================================ */

.contact-grid {

    display: grid;

    grid-template-columns:
        repeat(auto-fit, minmax(220px, 1fr));

    gap: 15px;

}


.contact-box {

    padding: 20px;

    background: #f8fafc;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

}


.contact-box h3 {

    margin-top: 0;

    color: #2563eb;

}


/* ============================================================
   DOWNLOAD
   ============================================================ */

.download-section {

    text-align: center;

    margin: 30px 0;

}


.download-button {

    display: inline-block;

    padding: 15px 30px;

    background: #0f172a;

    color: white;

    text-decoration: none;

    border-radius: 10px;

    font-size: 16px;

    font-weight: bold;

}


.download-button:hover {

    background: #1e293b;

}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    background: #0f172a;

    color: #cbd5e1;

    text-align: center;

    padding: 25px;

    line-height: 1.7;

}


.footer strong {

    color: #38bdf8;

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    .hero {

        padding: 50px 5%;

    }


    .hero h1 {

        font-size: 30px;

    }


    .container {

        width: 92%;

    }


    .navbar {

        padding: 15px 5%;

    }


    .nav-text {

        display: none;

    }

}

</style>

</head>


<body>


<!-- ============================================================
     NAVBAR
     ============================================================ -->

<div class="navbar">

    <div class="logo">

        TechNova™

    </div>


    <div class="nav-text">

        Official Customer Support Portal

    </div>

</div>


<!-- ============================================================
     HERO
     ============================================================ -->

<section class="hero">

    <span class="company-label">

        TechNova Solutions Pvt. Ltd.

    </span>


    <h1>

        How can we help you?

    </h1>


    <p>

        Welcome to the TechNova customer support portal.
        Our AI-powered support system automatically
        understands your request and connects it with
        the appropriate support specialist.

    </p>

</section>


<!-- ============================================================
     MAIN
     ============================================================ -->

<div class="container">


<!-- ============================================================
     AI SUPPORT TEAM
     ============================================================ -->

<div class="card">

    <h2>

        🤖 Our AI Support Team

    </h2>


    <div class="agents">


        <div class="agent billing">

            <div class="agent-icon">

                💳

            </div>

            <h3>

                Billing Agent

            </h3>

            <p>

                Payments, invoices,
                subscriptions and charges.

            </p>

        </div>


        <div class="agent technical">

            <div class="agent-icon">

                🔧

            </div>

            <h3>

                Technical Agent

            </h3>

            <p>

                Login, errors, bugs
                and technical issues.

            </p>

        </div>


        <div class="agent refund">

            <div class="agent-icon">

                💰

            </div>

            <h3>

                Refund Agent

            </h3>

            <p>

                Refunds, cancellations
                and money-back requests.

            </p>

        </div>


        <div class="agent general">

            <div class="agent-icon">

                💬

            </div>

            <h3>

                General Agent

            </h3>

            <p>

                General customer
                questions and assistance.

            </p>

        </div>


    </div>

</div>


<!-- ============================================================
     CUSTOMER QUERY
     ============================================================ -->

<div class="card">

    <h2>

        📩 Submit a Support Request

    </h2>


    <p>

        Describe your issue below. The TechNova AI
        Support Router will automatically assign
        your request to the correct support agent.

    </p>


    <form method="POST">

        <textarea
            name="query"
            placeholder="Example: I was charged twice for my subscription..."
            required
        >{{ query }}</textarea>


        <br>


        <button type="submit">

            🚀 Get Support

        </button>

    </form>


    {% if error %}

    <div class="error">

        ❌ {{ error }}

    </div>

    {% endif %}


    {% if agent_name %}

    <div class="selected-agent">

        <h3>

            🎯 Request Assigned

        </h3>


        <div class="agent-name">

            {{ agent_name }}

        </div>

    </div>

    {% endif %}


    {% if response %}

    <div class="response">

        <h3>

            🤖 TechNova AI Response

        </h3>


        <div class="ai-text">

            {{ response }}

        </div>

    </div>

    {% endif %}

</div>


<!-- ============================================================
     CONTACT INFORMATION
     ============================================================ -->

<div class="card">

    <h2>

        📞 TechNova Support Center

    </h2>


    <div class="contact-grid">


        <!-- PHONE -->

        <div class="contact-box">

            <h3>

                ☎️ Helpline

            </h3>


            <a
                href="{{ phone_link }}"
                class="support-link call-link"
            >

                📞 {{ phone }}

            </a>

        </div>


        <!-- EMAIL -->

        <div class="contact-box">

            <h3>

                📧 Email

            </h3>


            <a
                href="{{ email_link }}"
                class="support-link email-link"
            >

                ✉️ {{ email }}

            </a>

        </div>


        <!-- WEBSITE -->

        <div class="contact-box">

            <h3>

                🌐 Website

            </h3>


            <a
                href="{{ website }}"
                target="_blank"
                class="support-link website-link"
            >

                🌐 Visit Website

            </a>

        </div>


        <!-- WORKING HOURS -->

        <div class="contact-box">

            <h3>

                🕒 Working Hours

            </h3>


            <p>

                {{ working_hours }}

            </p>

        </div>


    </div>

</div>


<!-- ============================================================
     DOWNLOAD CURRENT REQUEST
     ============================================================ -->

{% if response %}

<div class="download-section">

    <a
        href="/download"
        class="download-button"
    >

        ⬇️ Download This Response

    </a>

</div>

{% endif %}


</div>


<!-- ============================================================
     FOOTER
     ============================================================ -->

<div class="footer">

    <strong>

        TechNova Solutions Pvt. Ltd.

    </strong>

    <br>

    AI-Powered Customer Support System

    <br>

    © 2026 TechNova Solutions. All Rights Reserved.

</div>


</body>

</html>

"""


# ============================================================
# HOME ROUTE
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    query = ""

    agent_name = None

    response = None

    error = None


    if request.method == "POST":

        query = request.form.get(
            "query",
            ""
        ).strip()


        # ----------------------------------------------------
        # INPUT GUARDRAIL
        # ----------------------------------------------------

        valid, message = input_guardrail(query)


        if not valid:

            error = message

        else:

            try:

                # ------------------------------------------------
                # ROUTER AGENT
                # ------------------------------------------------

                agent_name = router_agent(query)


                # ------------------------------------------------
                # GET SPECIALIZED AGENT
                # ------------------------------------------------

                agent = AGENTS.get(agent_name)


                if agent is None:

                    error = "Agent not found."

                else:

                    # --------------------------------------------
                    # GENERATE AI RESPONSE
                    # --------------------------------------------

                    response = agent(query)


                    # --------------------------------------------
                    # STORE MEMORY
                    # --------------------------------------------

                    memory.append({

                        "query": query,

                        "agent": agent_name,

                        "response": response

                    })


                    # Keep latest 50 conversations

                    if len(memory) > 50:

                        memory.pop(0)


            except Exception as e:

                error = "AI service error: " + str(e)


    return render_template_string(

        HTML,

        query=query,

        agent_name=agent_name,

        response=response,

        error=error,

        phone=PHONE,

        phone_link=PHONE_LINK,

        email=EMAIL,

        email_link=EMAIL_LINK,

        website=WEBSITE,

        working_hours=WORKING_HOURS

    )


# ============================================================
# DOWNLOAD CURRENT REQUEST
# ============================================================

@app.route("/download")
def download_page():

    # --------------------------------------------------------
    # Check whether there is a conversation
    # --------------------------------------------------------

    if not memory:

        return """
        <html>
        <head>
            <title>No Response</title>
        </head>

        <body style="
            font-family: Arial;
            padding: 40px;
            text-align: center;
        ">

            <h2>No support response available.</h2>

            <p>
                Please submit a support request first.
            </p>

            <a href="/">
                Return to Support Page
            </a>

        </body>
        </html>
        """


    # --------------------------------------------------------
    # Get latest conversation
    # --------------------------------------------------------

    latest = memory[-1]

    customer_query = latest["query"]

    selected_agent = latest["agent"]

    ai_response = latest["response"]


    # --------------------------------------------------------
    # Escape text for HTML
    # --------------------------------------------------------

    safe_query = html.escape(customer_query)

    safe_agent = html.escape(selected_agent)

    safe_response = html.escape(ai_response)

    safe_company = html.escape(COMPANY_NAME)

    safe_phone = html.escape(PHONE)

    safe_email = html.escape(EMAIL)

    safe_hours = html.escape(WORKING_HOURS)


    # --------------------------------------------------------
    # Create exact printable response page
    # --------------------------------------------------------

    download_html = f"""

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>TechNova Support Response</title>


<style>

body {{

    font-family: Arial, Helvetica, sans-serif;

    background: #f1f5f9;

    margin: 0;

    padding: 30px;

    color: #1e293b;

}}


.page {{

    max-width: 900px;

    margin: auto;

    background: white;

    padding: 40px;

    border-radius: 15px;

    box-shadow:
        0 5px 20px rgba(0,0,0,0.10);

}}


.header {{

    background: #0f172a;

    color: white;

    padding: 25px;

    border-radius: 12px;

    text-align: center;

}}


.header h1 {{

    color: #38bdf8;

    margin: 0 0 10px 0;

}}


.section {{

    margin-top: 25px;

    padding: 20px;

    border: 1px solid #e2e8f0;

    border-radius: 12px;

    background: #f8fafc;

}}


.section h2 {{

    color: #1d4ed8;

    margin-top: 0;

}}


.query {{

    background: #eff6ff;

    border-left: 5px solid #2563eb;

}}


.agent {{

    background: #dcfce7;

    border-left: 5px solid #16a34a;

}}


.answer {{

    background: #f8fafc;

    border-left: 5px solid #7c3aed;

    white-space: pre-line;

    line-height: 1.7;

}}


.contact a {{

    display: inline-block;

    padding: 10px 15px;

    margin: 5px;

    color: white;

    text-decoration: none;

    border-radius: 7px;

    font-weight: bold;

}}


.call {{

    background: #2563eb;

}}


.email {{

    background: #7c3aed;

}}


.website {{

    background: #16a34a;

}}


.footer {{

    margin-top: 30px;

    padding: 20px;

    background: #0f172a;

    color: #cbd5e1;

    text-align: center;

    border-radius: 10px;

}}


@media print {{

    body {{

        background: white;

        padding: 0;

    }}


    .page {{

        box-shadow: none;

        max-width: 100%;

    }}

}}

</style>

</head>


<body>


<div class="page">


<div class="header">

    <h1>

        TechNova Solutions

    </h1>

    <div>

        Customer Support Response

    </div>

</div>


<!-- CUSTOMER REQUEST -->

<div class="section query">

    <h2>

        📩 Customer Request

    </h2>


    <p>

        {safe_query}

    </p>

</div>


<!-- SELECTED AGENT -->

<div class="section agent">

    <h2>

        🎯 Assigned Support Agent

    </h2>


    <p>

        <strong>

            {safe_agent}

        </strong>

    </p>

</div>


<!-- AI RESPONSE -->

<div class="section answer">

    <h2>
        🤖 TechNova AI Response
    </h2>


    <div>

        {safe_response}

    </div>

</div>


<!-- SUPPORT CENTER -->

<div class="section contact">

    <h2>

        📞 TechNova Support Center

    </h2>


    <p>

        <strong>Helpline:</strong>

    </p>


    <a
        href="{PHONE_LINK}"
        class="call"
    >

        📞 {safe_phone}

    </a>


    <p>

        <strong>Email:</strong>

    </p>


    <a
        href="{EMAIL_LINK}"
        class="email"
    >

        ✉️ {safe_email}

    </a>


    <p>

        <strong>Website:</strong>

    </p>


    <a
        href="{WEBSITE}"
        target="_blank"
        class="website"
    >

        🌐 Visit Website

    </a>


    <p>

        <strong>Working Hours:</strong>

        {safe_hours}

    </p>

</div>


<!-- FOOTER -->

<div class="footer">

    <strong>

        {safe_company}

    </strong>


    <br>


    AI-Powered Customer Support System


    <br>


    © 2026 TechNova Solutions. All Rights Reserved.

</div>


</div>


</body>

</html>

"""


    # --------------------------------------------------------
    # SEND FILE FOR DOWNLOAD
    # --------------------------------------------------------

    file_response = make_response(download_html)


    file_response.headers["Content-Type"] = (
        "text/html; charset=utf-8"
    )


    file_response.headers["Content-Disposition"] = (
        "attachment; "
        "filename=technova_support_response.html"
    )


    return file_response


# ============================================================
# MEMORY PAGE
# ============================================================

@app.route("/memory")
def show_memory():

    return render_template_string(

        """
<!DOCTYPE html>

<html>

<head>

<title>TechNova Memory</title>


<style>

body {

    font-family: Arial;

    background: #f1f5f9;

    padding: 30px;

}


h1 {

    color: #1d4ed8;

}


.memory {

    background: white;

    padding: 20px;

    margin: 15px 0;

    border-radius: 12px;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.1);

}


.back {

    display: inline-block;

    margin-top: 20px;

    padding: 12px 20px;

    background: #2563eb;

    color: white;

    text-decoration: none;

    border-radius: 8px;

}

</style>

</head>


<body>


<h1>

    🧠 TechNova Conversation Memory

</h1>


{% if memory %}


    {% for item in memory %}

    <div class="memory">


        <b>Customer Query:</b>

        <p>

            {{ item.query }}

        </p>


        <b>Selected Agent:</b>

        <p>

            {{ item.agent }}

        </p>


        <b>AI Response:</b>

        <p style="white-space: pre-line;">

            {{ item.response }}

        </p>


    </div>

    {% endfor %}


{% else %}


    <p>

        No conversations stored yet.

    </p>


{% endif %}


<a href="/" class="back">

    ← Back to Support

</a>


</body>

</html>
        """,

        memory=memory

    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()

    print("==============================================")

    print("       TECHNOVA CUSTOMER SUPPORT")

    print("==============================================")

    print()

    print("Company: TechNova Solutions Pvt. Ltd.")

    print()

    print("Open in browser:")

    print("http://127.0.0.1:5000")

    print()

    print("Memory page:")

    print("http://127.0.0.1:5000/memory")

    print()

    print("Server running...")

    print("==============================================")


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False,

        use_reloader=False

    )