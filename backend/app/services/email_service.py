"""
Email Service - Send HTML emails with templates.

Supports Gmail, Outlook, Yahoo, and other SMTP services.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


# Email templates
EMAIL_TEMPLATES = {
    "welcome": """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 32px; font-weight: 700; }}
            .content {{ padding: 40px; }}
            .content p {{ color: #333333; font-size: 16px; line-height: 1.6; margin: 20px 0; }}
            .button {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 16px 32px; border-radius: 30px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
            .features {{ display: flex; gap: 20px; margin: 30px 0; }}
            .feature {{ flex: 1; background: #f8f9fa; padding: 20px; border-radius: 12px; text-align: center; }}
            .feature-icon {{ font-size: 32px; margin-bottom: 10px; }}
            .feature h3 {{ color: #333333; margin: 10px 0; font-size: 14px; }}
            .footer {{ background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e9ecef; }}
            .footer p {{ color: #6c757d; font-size: 14px; margin: 5px 0; }}
            .social {{ margin: 20px 0; }}
            .social a {{ color: #667eea; margin: 0 10px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>ResumeGPT</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">AI Resume Analyzer & ATS Booster</p>
            </div>
            <div class="content">
                <p>Hi <strong>{name}</strong>,</p>
                <p>Welcome to <strong>ResumeGPT</strong>! Your AI-powered resume analyzer is ready to help you land your dream job.</p>
                
                <center><a href="{app_url}" class="button">Get Started</a></center>
                
                <div class="features">
                    <div class="feature">
                        <div class="feature-icon">📊</div>
                        <h3>ATS Scoring</h3>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">✍️</div>
                        <h3>AI Rewrites</h3>
                    </div>
                    <div class="feature">
                        <div class="feature-icon">📝</div>
                        <h3>Cover Letters</h3>
                    </div>
                </div>
                
                <p>With ResumeGPT, you can:</p>
                <ul style="color: #333333; line-height: 1.8;">
                    <li>Analyze your resume against job descriptions</li>
                    <li>Get AI-powered bullet point rewrites</li>
                    <li>Compare resume versions with A/B testing</li>
                    <li>Track your job applications</li>
                </ul>
            </div>
            <div class="footer">
                <p>Best regards,<br>The ResumeGPT Team</p>
                <div class="social">
                    <a href="{app_url}">Website</a> | <a href="{app_url}">Support</a>
                </div>
                <p style="font-size: 12px; color: #adb5bd;">© 2026 ResumeGPT. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """,
    "cover_letter": """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; }}
            .content p {{ color: #333333; font-size: 16px; line-height: 1.6; }}
            .cover-letter {{ background: #f8f9fa; padding: 30px; border-radius: 12px; border-left: 4px solid #667eea; margin: 20px 0; white-space: pre-line; }}
            .company {{ color: #667eea; font-weight: 600; }}
            .button {{ display: inline-block; background: #667eea; color: #ffffff; padding: 14px 28px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 20px 10px 20px 0; }}
            .footer {{ background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e9ecef; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Cover Letter</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Professionally generated just for you!</p>
            </div>
            <div class="content">
                <p>Hi <strong>{name}</strong>,</p>
                <p>Your cover letter for <span class="company">{company}</span> is ready!</p>
                
                <div class="cover-letter">{cover_letter}</div>
                
                <center>
                    <a href="{download_link}" class="button">Download DOCX</a>
                    <a href="{app_url}" class="button" style="background: #764ba2;">View ResumeGPT</a>
                </center>
            </div>
            <div class="footer">
                <p>© 2026 ResumeGPT - Land your dream job faster!</p>
            </div>
        </div>
    </body>
    </html>
    """,
    "callback_alert": """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); padding: 40px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; }}
            .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0; }}
            .stat {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; text-align: center; color: #ffffff; }}
            .stat-value {{ font-size: 36px; font-weight: 700; }}
            .stat-label {{ font-size: 14px; opacity: 0.9; }}
            .details {{ background: #f8f9fa; padding: 20px; border-radius: 12px; margin: 20px 0; }}
            .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #e9ecef; }}
            .detail-label {{ color: #6c757d; }}
            .detail-value {{ font-weight: 600; color: #333; }}
            .winner {{ color: #27ae60; font-weight: 700; }}
            .button {{ display: inline-block; background: #667eea; color: #ffffff; padding: 14px 28px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
            .footer {{ background: #f8f9fa; padding: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Callback Alert!</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Your resume is working!</p>
            </div>
            <div class="content">
                <p>Hi <strong>{name}</strong>,</p>
                <p>Great news! One of your resume versions received a callback.</p>
                
                <div class="stats">
                    <div class="stat">
                        <div class="stat-value">{total_tests}</div>
                        <div class="stat-label">Total Tests</div>
                    </div>
                    <div class="stat">
                        <div class="stat-value">{callback_rate}%</div>
                        <div class="stat-label">Callback Rate</div>
                    </div>
                </div>
                
                <div class="details">
                    <div class="detail-row">
                        <span class="detail-label">Winner</span>
                        <span class="detail-value winner">{winner}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Platform</span>
                        <span class="detail-value">{platform}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Best Score</span>
                        <span class="detail-value">{best_score}</span>
                    </div>
                </div>
                
                <center><a href="{app_url}/ab-tests" class="button">View All Tests</a></center>
            </div>
            <div class="footer">
                <p>© 2026 ResumeGPT - Keep optimizing!</p>
            </div>
        </div>
    </body>
    </html>
    """,
    "job_alert": """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 20px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #f39c12 0%, #e74c3c 100%); padding: 40px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 28px; }}
            .content {{ padding: 40px; }}
            .job-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; margin: 20px 0; color: #ffffff; }}
            .job-title {{ font-size: 20px; font-weight: 700; margin: 0 0 10px 0; }}
            .job-company {{ font-size: 16px; opacity: 0.9; }}
            .job-details {{ margin: 15px 0; opacity: 0.9; font-size: 14px; }}
            .salary {{ background: rgba(255,255,255,0.2); padding: 10px 15px; border-radius: 8px; display: inline-block; margin-top: 10px; }}
            .button {{ display: inline-block; background: #ffffff; color: #667eea; padding: 14px 28px; border-radius: 25px; text-decoration: none; font-weight: 600; margin: 20px 10px 20px 0; }}
            .footer {{ background: #f8f9fa; padding: 30px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 Job Application Update</h1>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0;">Your application status has changed</p>
            </div>
            <div class="content">
                <p>Hi <strong>{name}</strong>,</p>
                
                <div class="job-card">
                    <div class="job-title">{position}</div>
                    <div class="job-company">{company}</div>
                    <div class="job-details">
                        📍 {location}<br>
                        📅 Applied: {applied_date}
                    </div>
                    <div class="salary">💰 {salary}</div>
                </div>
                
                <p style="font-size: 18px;">Status: <strong style="color: #27ae60;">{status}</strong></p>
                
                <center>
                    <a href="{job_url}" class="button">View Job</a>
                    <a href="{app_url}/tracker" class="button" style="background: #764ba2;">All Applications</a>
                </center>
            </div>
            <div class="footer">
                <p>© 2026 ResumeGPT - Track your job search!</p>
            </div>
        </div>
    </body>
    </html>
    """,
}


def get_smtp_config() -> Dict[str, str]:
    """Get SMTP configuration from environment."""
    return {
        "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "port": int(os.getenv("SMTP_PORT", "587")),
        "username": os.getenv("SMTP_USERNAME", ""),
        "password": os.getenv("SMTP_PASSWORD", ""),
        "from": os.getenv("EMAIL_FROM", "ResumeGPT <noreply@resumegpt.com>"),
    }


def is_email_configured() -> bool:
    """Check if email is properly configured."""
    config = get_smtp_config()
    return bool(config["username"] and config["password"])


def render_template(template_name: str, data: Dict) -> str:
    """Render an email template with data."""
    template = EMAIL_TEMPLATES.get(template_name, "")

    # Add common data
    data.setdefault("app_url", os.getenv("APP_URL", "http://localhost:3000"))
    data.setdefault("name", data.get("name", "User"))

    # Simple template rendering
    result = template
    for key, value in data.items():
        result = result.replace("{" + key + "}", str(value))

    return result


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    plain_text: str = None,
) -> bool:
    """
    Send an email via SMTP.

    Returns True if successful, False otherwise.
    """
    config = get_smtp_config()

    if not config["username"] or not config["password"]:
        print("Email not configured - skipping send")
        return False

    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config["from"]
        msg["To"] = to_email

        # Add plain text version
        if plain_text:
            text_part = MIMEText(plain_text, "plain")
            msg.attach(text_part)

        # Add HTML version
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        # Connect to SMTP and send
        server = smtplib.SMTP(config["host"], config["port"])
        server.starttls()
        server.login(config["username"], config["password"])
        server.sendmail(config["from"], [to_email], msg.as_string())
        server.quit()

        print(f"Email sent to {to_email}: {subject}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_welcome_email(to_email: str, name: str) -> bool:
    """Send welcome email."""
    html = render_template("welcome", {"name": name})
    plain = f"Welcome to ResumeGPT! Your AI resume analyzer is ready. Get started at {os.getenv('APP_URL')}"
    return send_email(to_email, "Welcome to ResumeGPT! 🎉", html, plain)


def send_cover_letter_email(
    to_email: str, name: str, company: str, cover_letter: str
) -> bool:
    """Send generated cover letter."""
    html = render_template(
        "cover_letter",
        {
            "name": name,
            "company": company,
            "cover_letter": cover_letter[:500] + "...",
            "download_link": f"{os.getenv('APP_URL')}/downloads",
        },
    )
    plain = f"Your cover letter for {company} is ready!"
    return send_email(to_email, f"Your Cover Letter for {company}", html, plain)


def send_callback_alert(
    to_email: str,
    name: str,
    total_tests: int,
    callback_rate: float,
    winner: str,
    platform: str,
    best_score: float,
) -> bool:
    """Send callback alert email."""
    html = render_template(
        "callback_alert",
        {
            "name": name,
            "total_tests": total_tests,
            "callback_rate": callback_rate,
            "winner": winner.upper(),
            "platform": platform,
            "best_score": f"{best_score:.0f}/100",
        },
    )
    plain = (
        f"Great news! Your resume received a callback! {callback_rate}% callback rate."
    )
    return send_email(to_email, "🎉 Callback Alert! Your Resume Worked!", html, plain)


def send_job_alert(
    to_email: str,
    name: str,
    company: str,
    position: str,
    location: str,
    salary: str,
    status: str,
    applied_date: str,
    job_url: str,
) -> bool:
    """Send job application update."""
    html = render_template(
        "job_alert",
        {
            "name": name,
            "company": company,
            "position": position,
            "location": location,
            "salary": salary,
            "status": status,
            "applied_date": applied_date,
            "job_url": job_url,
        },
    )
    plain = f"Job Application Update: {position} at {company} - {status}"
    return send_email(to_email, f"📋 Job Update: {position}", html, plain)
