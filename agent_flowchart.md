Sample demonstration of the three workflows.
1.	The first one – answers employee questions from a knowledge base, 
2.	The second – creates Jira support tickets when it does not have an answer, 
3.	The third – checks ticket status on demand.

TERMINAL Display

(venv) PS C:\Temp\! 0 Coursers\z_github-projects\SmartDesk_AI> python src/agents/agent.py

============================================================
  SmartDesk AI - Intelligent IT & HR Operations Agent
  Roadmap Consulting Internal Support
============================================================

Type your question and press Enter.
Type 'quit' or 'exit' to end the session.
Type 'new' to start a fresh conversation.
------------------------------------------------------------

SmartDesk : Hello! I am SmartDesk AI, your IT and HR support assistant at Roadmap Consulting.

I can help you with:
  IT support questions (passwords, VPN, MFA, email)
  HR policy questions (leave, WFH, reimbursement)
  Creating support tickets for issues I cannot solve
  Checking the status of your existing tickets

How can I help you today?
You        : How do I reset my password?

SmartDesk : To reset your password, please follow these steps:

1. Go to [https://passwords.roadmapconsulting.com].
2. Select "Forgot Password" or "Reset Password."
3. Enter your Roadmap Consulting username or work email address.
4. Complete the identity verification steps (you may be asked to verify using MFA, receive a verification code, or answer security questions if configured).
5. Enter a new password that meets Roadmap Consulting password requirements.
6. Confirm the new password.
7. Submit the change.
8. Wait for confirmation that the password reset was successful.
9. Sign in again using your new password.

After resetting your password, remember to update it anywhere it may be saved, such as in your Windows or Mac sign-in, mobile email app, VPN client, Microsoft Teams, browser-saved passwords, mapped drives, or any application that uses your Roadmap Consulting account.

Is there anything else I can help with?
You        : How many casual leave days do I get per year?

SmartDesk : Eligible full-time employees receive 8 Casual Leave days per calendar year. Casual Leave may be taken as a full day, half day, or hourly increment if approved by the manager and supported by the Leave Management System. 

Is there anything else I can help with?

Sources: knowledge_base/hr_qa.json, knowledge_base/hr_leave_policy.md

You        : My monitor keeps flickering

SmartDesk : I am sorry I could not find information about that in my knowledge base.

I can create a support ticket for the team to look into this for you.

Could you please share your work email address so I can look that up for you?
You        : demo@roadmapconsulting.com

SmartDesk : I would like to create a support ticket for you.

Please review the details below:

----------------------------------------
  📋 Title    : My monitor keeps flickering
  🏷  Category : IT Support
  📧 Email    : demo@roadmapconsulting.com
  🤖 Created by: SmartDesk AI Agent
----------------------------------------

Shall I go ahead and create this ticket?
Type YES to confirm or NO to cancel.
You        : yes

SmartDesk : Your support ticket has been created successfully!

  Ticket ID  : SSDAI-42
  Title      : My monitor keeps flickering
  URL        : https://oe7051.atlassian.net/browse/SSDAI-42

The support team will review your ticket and get back to you shortly.

Is there anything else I can help you with?
You        : What is the status of my tickets?

SmartDesk : I found 4 ticket(s) for demo@roadmapconsulting.com:

🎫 SSDAI-42 : My monitor keeps flickering
   📊 Status  : To Do
   📅 Created : 2026-06-12
   🔗 Link    : https://oe7051.atlassian.net/browse/SSDAI-42

🎫 SSDAI-41 : My Monitor keeps flickering
   📊 Status  : To Do
   📅 Created : 2026-06-12
   🔗 Link    : https://oe7051.atlassian.net/browse/SSDAI-41

🎫 SSDAI-40 : My monitor is flickering
   📊 Status  : To Do
   📅 Created : 2026-06-12
   🔗 Link    : https://oe7051.atlassian.net/browse/SSDAI-40

🎫 SSDAI-39 : My monitor keeps flickering
   📊 Status  : To Do
   📅 Created : 2026-06-11
   🔗 Link    : https://oe7051.atlassian.net/browse/SSDAI-39
Is there anything else I can help you with?
You        : no

SmartDesk : You are welcome! Have a great day.
Feel free to come back any time you need help.

Enter your question or enter exit/quit to end the session.
You        : quit

SmartDesk : Thank you for using SmartDesk AI.
           Have a great day!


