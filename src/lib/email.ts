import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)
const FROM = process.env.FROM_EMAIL ?? 'signals@gethigh.life'

export async function sendWelcomeEmail(email: string, alias?: string) {
  try {
    await resend.emails.send({
      from: FROM,
      to: email,
      subject: 'You found the door. Now don\'t lose it.',
      html: `
        <div style="background:#080808;color:#e8e8e8;font-family:monospace;padding:40px;max-width:600px;">
          <h1 style="color:#00ff41;letter-spacing:0.1em;">COLD EMPIRE</h1>
          <p style="color:#888;font-size:12px;letter-spacing:0.2em;">SIGNAL RECEIVED</p>
          <hr style="border-color:#2a2a2a;margin:24px 0;" />
          <h2 style="color:#e8e8e8;">Welcome, ${alias ?? 'Stranger'}.</h2>
          <p>You found the door. Most people walk past it.</p>
          <p>Here is what comes next:</p>
          <ul style="color:#888;line-height:2;">
            <li>Read the Cold Code — 13 articles. Start at Article I.</li>
            <li>Join the Discord — The lobby is open.</li>
            <li>Complete your first mission — Earn your first rank.</li>
          </ul>
          <a href="${process.env.NEXTAUTH_URL}/cold-code" style="display:inline-block;background:#00ff41;color:#080808;padding:12px 24px;text-decoration:none;font-weight:bold;margin-top:24px;">Read the Cold Code</a>
          <p style="color:#444;font-size:11px;margin-top:40px;">Cold Empire — GetHigh.life</p>
        </div>
      `,
    })
  } catch {
    // Email failure is non-fatal
  }
}

export async function sendOrderConfirmEmail(email: string, orderItems: string) {
  try {
    await resend.emails.send({
      from: FROM,
      to: email,
      subject: 'Package secured.',
      html: `
        <div style="background:#080808;color:#e8e8e8;font-family:monospace;padding:40px;max-width:600px;">
          <h1 style="color:#00ff41;letter-spacing:0.1em;">COLD EMPIRE</h1>
          <p style="color:#888;font-size:12px;letter-spacing:0.2em;">ORDER CONFIRMED</p>
          <hr style="border-color:#2a2a2a;margin:24px 0;" />
          <h2 style="color:#e8e8e8;">Package secured.</h2>
          <p>Watch your inbox. The signal continues there.</p>
          <p style="color:#888;">Order: ${orderItems}</p>
          <hr style="border-color:#2a2a2a;margin:24px 0;" />
          <p>While you wait:</p>
          <a href="${process.env.NEXTAUTH_URL}/cold-code" style="display:inline-block;background:#00ff41;color:#080808;padding:12px 24px;text-decoration:none;font-weight:bold;margin-top:8px;">Read the Cold Code</a>
          <p style="color:#444;font-size:11px;margin-top:40px;">Cold Empire — GetHigh.life</p>
        </div>
      `,
    })
  } catch {
    // Email failure is non-fatal
  }
}

export async function sendCartelRequestEmail(email: string) {
  try {
    await resend.emails.send({
      from: FROM,
      to: email,
      subject: 'Request received. Watch for the next signal.',
      html: `
        <div style="background:#080808;color:#e8e8e8;font-family:monospace;padding:40px;max-width:600px;">
          <h1 style="color:#00ff41;letter-spacing:0.1em;">COLD CARTEL</h1>
          <p style="color:#888;font-size:12px;letter-spacing:0.2em;">ACCESS REQUEST RECEIVED</p>
          <hr style="border-color:#2a2a2a;margin:24px 0;" />
          <h2 style="color:#e8e8e8;">Everybody wants the room.</h2>
          <p>Not everybody understands the code.</p>
          <p>Your request has been logged. If you are serious about it, read the code while you wait.</p>
          <a href="${process.env.NEXTAUTH_URL}/cold-code" style="display:inline-block;background:#00ff41;color:#080808;padding:12px 24px;text-decoration:none;font-weight:bold;margin-top:24px;">Read the Cold Code</a>
          <p style="color:#444;font-size:11px;margin-top:40px;">Cold Cartel — Part of Cold Empire</p>
        </div>
      `,
    })
  } catch {
    // Email failure is non-fatal
  }
}
