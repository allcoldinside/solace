'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useSession } from 'next-auth/react'
import { useRouter } from 'next/navigation'

// ─── GOOGLE FONTS ─────────────────────────────────────────────────────────────
const FONTS_URL =
  'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Special+Elite&display=swap'

// ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
const GLOBAL_CSS = `
  .capp *, .capp *::before, .capp *::after { box-sizing: border-box; }
  :root {
    --bg:        #080806;
    --bg2:       #0e0e0b;
    --bg3:       #141410;
    --fg:        #e8e4d9;
    --dim:       #5a5850;
    --dim2:      #3a3830;
    --border:    #222018;
    --border2:   #2e2c26;
    --green:     #3d7a45;
    --green-b:   #5aad65;
    --green-d:   #1a3520;
    --amber:     #c8a840;
    --amber-d:   #6b5820;
    --amber-dim: #2a2010;
    --blue:      #2a4a6b;
    --blue-b:    #4a8ab5;
    --blue-d:    #0e1e2e;
    --glow-g:    0 0 18px rgba(61,122,69,.55);
    --glow-a:    0 0 18px rgba(200,168,64,.4);
    --glow-b:    0 0 18px rgba(42,74,107,.55);
    --font-b:    'Bebas Neue', sans-serif;
    --font-m:    'Share Tech Mono', monospace;
    --font-s:    'EB Garamond', serif;
    --font-t:    'Special Elite', cursive;
    --nav-h:     60px;
  }

  /* Root container — full-viewport overlay */
  .capp {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: var(--bg);
    color: var(--fg);
    font-family: var(--font-m);
    overflow: hidden;
  }

  /* Grain */
  .capp::before {
    content: '';
    position: absolute; inset: 0; z-index: 9998; pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    opacity: 0.038;
  }

  /* Scanlines */
  .capp::after {
    content: '';
    position: absolute; inset: 0; z-index: 9997; pointer-events: none;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.055) 2px, rgba(0,0,0,0.055) 4px);
  }

  @keyframes fadeUp   { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }
  @keyframes fadeIn   { from{opacity:0} to{opacity:1} }
  @keyframes blink    { 50%{opacity:0} }
  @keyframes pulse    { 0%,100%{opacity:.6} 50%{opacity:1} }
  @keyframes glow-pulse-g { 0%,100%{box-shadow:var(--glow-g)} 50%{box-shadow:0 0 28px rgba(90,173,101,.7)} }
  @keyframes sweep    { 0%{background-position:0% -100%} 100%{background-position:0% 200%} }
  @keyframes spin     { to{transform:rotate(360deg)} }

  .capp .sweep-line {
    position: absolute; inset: 0; z-index: 9996; pointer-events: none;
    background: linear-gradient(
      0deg,
      transparent 0%, transparent 48%,
      rgba(90,173,101,0.04) 50%,
      transparent 52%, transparent 100%
    );
    background-size: 100% 200%;
    animation: sweep 6s linear infinite;
  }

  .capp .screen-scroll { overflow-y: auto; height: calc(100vh - var(--nav-h)); }
  .capp .screen-scroll::-webkit-scrollbar { width: 3px; }
  .capp .screen-scroll::-webkit-scrollbar-track { background: var(--bg); }
  .capp .screen-scroll::-webkit-scrollbar-thumb { background: var(--border2); }

  .capp .btn {
    font-family: var(--font-m);
    font-size: .55rem;
    letter-spacing: .18em;
    border: 1px solid var(--border2);
    color: var(--dim);
    background: none;
    padding: .6rem 1.2rem;
    cursor: pointer;
    transition: all .2s;
    text-transform: uppercase;
    border-radius: 0;
    margin: 0; padding: .6rem 1.2rem;
  }
  .capp .btn:hover { color: var(--fg); border-color: var(--fg); }
  .capp .btn-green { border-color: var(--green); color: var(--green-b); box-shadow: var(--glow-g); }
  .capp .btn-green:hover { background: var(--green-d); animation: glow-pulse-g 2s infinite; }
  .capp .btn-amber { border-color: var(--amber-d); color: var(--amber); box-shadow: var(--glow-a); }
  .capp .btn-amber:hover { background: var(--amber-dim); }
  .capp .btn-blue  { border-color: var(--blue); color: var(--blue-b); box-shadow: var(--glow-b); }

  .capp .rule { border: none; border-top: 1px solid var(--border); }

  .capp .label {
    font-family: var(--font-m);
    font-size: .44rem;
    letter-spacing: .24em;
    text-transform: uppercase;
    color: var(--dim);
  }
  .capp .label-green { color: var(--green); }
  .capp .label-amber { color: var(--amber); }
  .capp .label-blue  { color: var(--blue-b); }

  .capp .stat-cell { text-align: center; }
  .capp .stat-val  { font-family: var(--font-b); font-size: 1.5rem; color: var(--fg); line-height: 1; }
  .capp .stat-key  { font-family: var(--font-m); font-size: .38rem; letter-spacing: .2em; color: var(--dim); margin-top: .3rem; }

  .capp .feed-item {
    border-left: 2px solid var(--border);
    padding: .75rem 1rem;
    background: var(--bg2);
    margin-bottom: 1px;
    animation: fadeUp .3s ease;
  }
  .capp .feed-item-green { border-left-color: var(--green-b); }
  .capp .feed-item-amber { border-left-color: var(--amber); }
  .capp .feed-item-blue  { border-left-color: var(--blue-b); }

  .capp .coord-card {
    border: 1px solid var(--border);
    background: var(--bg2);
    padding: 1rem 1.25rem;
    margin-bottom: 1px;
    display: flex; align-items: center; gap: 1rem;
    cursor: pointer;
    transition: all .2s;
  }
  .capp .coord-card:hover          { border-color: var(--border2); background: var(--bg3); }
  .capp .coord-card-found          { border-color: var(--green-d); background: rgba(26,53,32,.3); }
  .capp .coord-card-locked         { border-color: var(--blue);    background: var(--blue-d); }
  .capp .coord-card-dim            { opacity: .35; pointer-events: none; }
`

// ─── STATIC DATA (mirrors site lore + ARG state) ──────────────────────────────
const FEED = [
  { id: 1, type: 'green', time: '03:47', text: 'COORD-04 · /signal · FREQUENCY LOCKED · 1 member found' },
  { id: 2, type: 'amber', time: '02:11', text: 'LORE DROP · Chapter IV unlocked · The Architecture of Smoke' },
  { id: 3, type: 'green', time: '01:58', text: 'CIPHER POOL · 18/25 fragments submitted · 7 remain' },
  { id: 4, type: 'blue',  time: '00:33', text: 'IB6 · SESSION 009 · 6 seats confirmed · 2 founding seats active' },
  { id: 5, type: 'green', time: 'yesterday', text: 'COORD-02 · /vi · ARTICLE VI DECODED · 4 members found' },
]

const COORDINATES = [
  { id: '01', slug: '/137',        name: 'THE FLASHLIGHT',  status: 'found'      },
  { id: '02', slug: '/vi',         name: 'ARTICLE VI',      status: 'found'      },
  { id: '03', slug: '/knock',      name: 'THE DOOR',        status: 'found'      },
  { id: '04', slug: '/signal',     name: 'THE SIGNAL',      status: 'active'     },
  { id: '05', slug: '/ghost',      name: 'THE GHOST',       status: 'active'     },
  { id: '06', slug: '/chalkboard', name: 'THE CHALKBOARD',  status: 'geo-locked' },
  { id: '07', slug: '/???',        name: 'UNKNOWN',         status: 'unreleased' },
]

const CHAPTERS = [
  { num: 'I',    title: 'THE BEGINNING OF THE COLD',    rank: null,      teaser: null,                                           siteSlug: 'the-door-is-earned' },
  { num: 'II',   title: 'THE ARCHITECTURE OF SMOKE',    rank: null,      teaser: null,                                           siteSlug: 'loyalty-builds-the-room' },
  { num: 'III',  title: 'WHY 13 AND 7',                 rank: null,      teaser: null,                                           siteSlug: 'the-signal-must-stay-clean' },
  { num: 'IV',   title: 'THE FOUNDING SEAT',            rank: 'ghost',   teaser: null,                                           siteSlug: 'family-eats-before-fame' },
  { num: 'V',    title: 'WHAT THE HOODIE MEANS',        rank: 'ghost',   teaser: null,                                           siteSlug: 'no-fake-smoke' },
  { num: 'VI',   title: 'THE CIPHER EXPLAINED',         rank: 'curator', teaser: 'The cipher was not designed to be solved alone.', siteSlug: 'respect-the-lobby' },
  { num: 'VII',  title: 'THE BACKROOM PROTOCOL',        rank: 'capo',    teaser: 'There are rooms inside rooms.',                 siteSlug: 'build-more-than-you-brag' },
  { num: 'VIII', title: "COLD'S RULES FOR THE FAMILY",  rank: 'capo',    teaser: 'Rules that were written before the drop.',     siteSlug: 'every-drop-has-meaning' },
]

// ─── INTERCEPT SCREEN ─────────────────────────────────────────────────────────
const INTERCEPT_LINES = [
  { text: 'COLD EMPIRE',       delay: 0    },
  { text: 'SIGNAL DETECTED.',  delay: 800  },
  { text: 'LOCATING...',       delay: 1600 },
  { text: '█████████████ 100%', delay: 2400 },
  { text: 'YOU HAVE BEEN FOUND.', delay: 3800 },
]

function InterceptScreen({ onEnter }: { onEnter: () => void }) {
  const [visible, setVisible] = useState<number[]>([])
  const [cursor, setCursor]   = useState(0)
  const [showRule, setShowRule] = useState(false)
  const [showSub, setShowSub]   = useState(false)
  const [showBtn, setShowBtn]   = useState(false)

  useEffect(() => {
    INTERCEPT_LINES.forEach((line, i) => {
      setTimeout(() => { setVisible(p => [...p, i]); setCursor(i) }, line.delay)
    })
    setTimeout(() => setShowRule(true), 5300)
    setTimeout(() => setShowSub(true),  5700)
    setTimeout(() => setShowBtn(true),  6400)
  }, [])

  return (
    <div style={{
      position: 'fixed', inset: 0,
      display: 'flex', flexDirection: 'column',
      justifyContent: 'center', alignItems: 'flex-start',
      padding: '2.5rem', background: 'var(--bg)', zIndex: 100,
    }}>
      <div style={{
        position: 'absolute', inset: 0, pointerEvents: 'none',
        background: 'radial-gradient(ellipse 60% 50% at 25% 50%, rgba(61,122,69,.04) 0%, transparent 70%)',
      }} />
      <div style={{ maxWidth: 520, width: '100%' }}>
        {INTERCEPT_LINES.map((line, i) => (
          <div key={i} style={{
            fontFamily: i === 0 ? 'var(--font-b)' : 'var(--font-m)',
            fontSize:   i === 0 ? 'clamp(1.8rem, 6vw, 2.8rem)' : '.72rem',
            letterSpacing: i === 0 ? '.08em' : '.12em',
            color: i === 0 ? 'var(--green-b)' : i === 4 ? 'var(--fg)' : 'var(--dim)',
            marginBottom: i === 0 ? '1.5rem' : '.5rem',
            opacity: visible.includes(i) ? 1 : 0,
            transform: visible.includes(i) ? 'none' : 'translateY(4px)',
            transition: 'opacity .3s ease, transform .3s ease',
            lineHeight: 1,
            ...(i === 0 && { textShadow: '0 0 30px rgba(90,173,101,.3)' }),
          }}>
            {line.text}
            {cursor === i && !showRule && (
              <span style={{
                display: 'inline-block', width: 2, height: '1em',
                background: 'var(--green-b)', marginLeft: 4,
                verticalAlign: 'middle', animation: 'blink 1s step-end infinite',
              }} />
            )}
          </div>
        ))}
        {showRule && <hr className="rule" style={{ marginTop: '1.5rem', marginBottom: '1.5rem', borderColor: 'var(--green-d)', animation: 'fadeIn .4s ease' }} />}
        {showSub && (
          <p style={{
            fontFamily: 'var(--font-t)', fontSize: '.78rem', lineHeight: 1.7,
            color: 'var(--dim)', fontStyle: 'italic', marginBottom: '2rem',
            animation: 'fadeUp .5s ease', maxWidth: 380,
          }}>
            This is not an app store download. You found this because you were supposed to.
          </p>
        )}
        {showBtn && (
          <button className="btn btn-green" onClick={onEnter}
            style={{ fontSize: '.65rem', padding: '.75rem 2rem', letterSpacing: '.22em', animation: 'fadeUp .4s ease' }}>
            ◆ ENTER
          </button>
        )}
      </div>
    </div>
  )
}

// ─── TOP BAR ──────────────────────────────────────────────────────────────────
function TopBar({ screen }: { screen: string }) {
  return (
    <div style={{
      height: 48, background: 'rgba(8,8,6,.97)',
      borderBottom: '1px solid var(--border)',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '0 1.25rem', flexShrink: 0, backdropFilter: 'blur(8px)',
    }}>
      <div style={{ fontFamily: 'var(--font-b)', fontSize: '.95rem', letterSpacing: '.08em' }}>
        <span style={{ color: 'var(--green-b)' }}>COLD</span>
        <span style={{ color: 'var(--dim2)', margin: '0 .3rem' }}>·</span>
        <span style={{ color: 'var(--dim)', fontSize: '.55rem', letterSpacing: '.2em' }}>{screen.toUpperCase()}</span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '.5rem' }}>
        <span style={{
          display: 'inline-block', width: 6, height: 6, borderRadius: '50%',
          background: 'var(--green-b)', boxShadow: '0 0 6px rgba(90,173,101,.8)',
          animation: 'pulse 2s infinite',
        }} />
        <span style={{ fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em', color: 'var(--green-b)' }}>◆ ACTIVE</span>
      </div>
    </div>
  )
}

// ─── BOTTOM NAV ───────────────────────────────────────────────────────────────
const NAV_ITEMS = [
  { id: 'home',   icon: '⌂', label: 'HOME'  },
  { id: 'arg',    icon: '◎', label: 'ARG'   },
  { id: 'lore',   icon: '≡', label: 'LORE'  },
  { id: 'ib6',    icon: '▣', label: 'IB6'   },
  { id: 'record', icon: '◈', label: 'REC'   },
]

function BottomNav({ active, onNav }: { active: string; onNav: (id: string) => void }) {
  return (
    <div style={{
      position: 'fixed', bottom: 0, left: 0, right: 0, height: 'var(--nav-h)',
      background: 'rgba(8,8,6,.98)', borderTop: '1px solid var(--border)',
      display: 'flex', zIndex: 200, backdropFilter: 'blur(12px)',
    }}>
      {NAV_ITEMS.map(item => {
        const isActive = active === item.id
        return (
          <button key={item.id} onClick={() => onNav(item.id)} style={{
            flex: 1, background: 'none', border: 'none', cursor: 'pointer',
            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
            gap: '.2rem', padding: 0,
            borderTop: isActive ? '2px solid var(--green-b)' : '2px solid transparent',
            transition: 'all .15s',
          }}>
            <span style={{
              fontSize: isActive ? '1rem' : '.85rem',
              color: isActive ? 'var(--green-b)' : 'var(--dim)',
              filter: isActive ? 'drop-shadow(0 0 4px rgba(90,173,101,.7))' : 'none',
              transition: 'all .15s', lineHeight: 1,
            }}>{item.icon}</span>
            <span style={{
              fontFamily: 'var(--font-m)', fontSize: '.32rem', letterSpacing: '.2em',
              color: isActive ? 'var(--green-b)' : 'var(--dim2)',
            }}>{item.label}</span>
          </button>
        )
      })}
    </div>
  )
}

// ─── WALLET CONNECT BUTTON ────────────────────────────────────────────────────
function WalletConnectBtn() {
  const [state, setState] = useState<'idle' | 'connecting' | 'connected'>('idle')

  const handle = () => {
    if (state === 'idle') {
      setState('connecting')
      setTimeout(() => setState('connected'), 1800)
    } else if (state === 'connected') {
      setState('idle')
    }
  }

  return (
    <button onClick={handle} className={`btn ${state === 'connected' ? 'btn-amber' : 'btn-green'}`}
      style={{ fontSize: '.42rem', padding: '.35rem .8rem' }}>
      {state === 'idle' ? 'CONNECT WALLET'
       : state === 'connecting' ? (
          <span style={{ display: 'flex', alignItems: 'center', gap: '.4rem' }}>
            <span style={{
              display: 'inline-block', width: 8, height: 8,
              border: '1px solid var(--green-b)', borderTopColor: 'transparent',
              borderRadius: '50%', animation: 'spin .8s linear infinite',
            }} />
            CONNECTING
          </span>
        ) : '◈ 0x3f9...A12b'}
    </button>
  )
}

// ─── HOME SCREEN ──────────────────────────────────────────────────────────────
interface HomeProps {
  callsign: string
  rank: string
  coordsFound: number
  points: number
}

function HomeScreen({ callsign, rank, coordsFound, points }: HomeProps) {
  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      {/* Member card */}
      <div style={{
        background: 'linear-gradient(135deg, var(--bg2) 0%, rgba(26,53,32,.25) 100%)',
        border: '1px solid var(--green-d)', padding: '1.5rem 1.25rem 1.25rem',
        position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', right: '-1rem', top: '-1rem',
          fontFamily: 'var(--font-b)', fontSize: '7rem',
          color: 'rgba(90,173,101,.035)', letterSpacing: '.05em',
          lineHeight: 1, pointerEvents: 'none', userSelect: 'none',
        }}>13/7</div>

        <div className="label label-amber" style={{ marginBottom: '.5rem' }}>FOUNDING MEMBER · SERIES 001</div>
        <div style={{
          fontFamily: 'var(--font-b)', fontSize: 'clamp(2rem,8vw,3rem)',
          letterSpacing: '.06em', color: 'var(--amber)', lineHeight: .9,
          textShadow: '0 0 30px rgba(200,168,64,.25)', marginBottom: '.5rem',
        }}>{callsign}</div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1px', background: 'var(--border)', border: '1px solid var(--border)', marginTop: '1.25rem' }}>
          {[
            { label: 'RANK',   val: rank.toUpperCase()  },
            { label: 'POINTS', val: points.toLocaleString() },
            { label: 'COORDS', val: `${coordsFound}/7`  },
          ].map(s => (
            <div key={s.label} className="stat-cell" style={{ background: 'var(--bg2)', padding: '.75rem .5rem' }}>
              <div className="stat-val" style={{ fontSize: '1.1rem' }}>{s.val}</div>
              <div className="stat-key">{s.label}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Wallet */}
      <div style={{
        padding: '.75rem 1.25rem', background: 'var(--bg3)', borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '.6rem' }}>
          <span style={{ fontSize: '.65rem', color: 'var(--dim)' }}>◎</span>
          <span style={{ fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em', color: 'var(--dim)' }}>CELO WALLET</span>
        </div>
        <WalletConnectBtn />
      </div>

      {/* Cipher pool */}
      <div style={{ padding: '.75rem 1.25rem', background: 'var(--bg2)', borderBottom: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '.5rem' }}>
          <div className="label">CIPHER POOL</div>
          <div className="label label-green">18 / 25</div>
        </div>
        <div style={{ height: 2, background: 'var(--border)', borderRadius: 1 }}>
          <div style={{
            height: '100%', width: `${(18/25)*100}%`,
            background: 'var(--green-b)', boxShadow: '0 0 6px rgba(90,173,101,.6)',
            borderRadius: 1, transition: 'width 1s ease',
          }} />
        </div>
        <div style={{ fontFamily: 'var(--font-t)', fontSize: '.58rem', color: 'var(--dim)', marginTop: '.5rem', fontStyle: 'italic' }}>
          7 fragments remain. The message is close.
        </div>
      </div>

      {/* Feed */}
      <div style={{ padding: '.75rem 1.25rem .5rem' }}>
        <div className="label" style={{ marginBottom: '.75rem' }}>// SIGNAL FEED</div>
      </div>
      {FEED.map(item => (
        <div key={item.id} className={`feed-item feed-item-${item.type}`}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '.3rem' }}>
            <span className={`label label-${item.type}`}>
              {item.type === 'green' ? '◆ SIGNAL' : item.type === 'amber' ? '◈ LORE' : '▣ IB6'}
            </span>
            <span className="label" style={{ color: 'var(--dim2)' }}>{item.time}</span>
          </div>
          <div style={{ fontFamily: 'var(--font-m)', fontSize: '.56rem', lineHeight: 1.6, color: 'var(--fg)', opacity: .85 }}>
            {item.text}
          </div>
        </div>
      ))}

      {/* Go to full site */}
      <div style={{ padding: '1.25rem', textAlign: 'center', borderTop: '1px solid var(--border)' }}>
        <a href="/hq" style={{
          fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em',
          color: 'var(--green-b)', textDecoration: 'none', textTransform: 'uppercase',
        }}>◆ ENTER COLD EMPIRE HQ →</a>
      </div>
    </div>
  )
}

// ─── ARG SCREEN ───────────────────────────────────────────────────────────────
interface ArgScreenProps {
  coordsFound: number
  onCoordTap: (coord: typeof COORDINATES[number]) => void
}

function ArgScreen({ coordsFound, onCoordTap }: ArgScreenProps) {
  const frags = ['M', '—', '—', 'G', '—', '—', '—']
  const found  = COORDINATES.filter(c => c.status === 'found').length

  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      <div style={{ padding: '1.25rem', background: 'var(--bg2)', borderBottom: '1px solid var(--border)' }}>
        <div className="label" style={{ marginBottom: '.6rem' }}>// MISSION CONTROL</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '.5rem' }}>
          <div className="label label-green">{found}/7 COORDINATES FOUND</div>
          <div className="label" style={{ color: 'var(--dim2)' }}>YOUR RECORD: {coordsFound}/7</div>
        </div>
        <div style={{ height: 2, background: 'var(--border)', marginBottom: '1rem' }}>
          <div style={{
            height: '100%', width: `${(found/7)*100}%`,
            background: 'var(--green-b)', boxShadow: '0 0 8px rgba(90,173,101,.5)',
          }} />
        </div>
        <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
          <div className="label" style={{ marginRight: '.4rem' }}>CIPHER:</div>
          {frags.map((f, i) => (
            <div key={i} style={{
              width: 28, height: 28,
              border: `1px solid ${f !== '—' ? 'var(--green)' : 'var(--border)'}`,
              background: f !== '—' ? 'var(--green-d)' : 'var(--bg)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: 'var(--font-b)', fontSize: '.85rem',
              color: f !== '—' ? 'var(--green-b)' : 'var(--dim2)',
              boxShadow: f !== '—' ? 'var(--glow-g)' : 'none',
            }}>{f}</div>
          ))}
        </div>
      </div>

      <div style={{ paddingTop: 1 }}>
        {COORDINATES.map(coord => (
          <CoordCard key={coord.id} coord={coord} onTap={() => coord.status !== 'unreleased' && onCoordTap(coord)} />
        ))}
      </div>

      <div style={{ padding: '1rem 1.25rem', borderTop: '1px solid var(--border)', marginTop: 1 }}>
        <div className="label" style={{ textAlign: 'center', color: 'var(--dim2)' }}>
          COMMUNITY PROGRESS · {found}/7 SIGNALS LOCATED
        </div>
      </div>
    </div>
  )
}

function CoordCard({ coord, onTap }: { coord: typeof COORDINATES[number]; onTap: () => void }) {
  const statusMap: Record<string, { label: string; cls: string; icon: string; color: string }> = {
    found:       { label: 'FOUND',      cls: 'coord-card-found',  icon: '◆', color: 'var(--green-b)' },
    active:      { label: 'ACTIVE',     cls: '',                  icon: '◎', color: 'var(--dim)'     },
    'geo-locked':{ label: 'GEO-LOCKED', cls: 'coord-card-locked', icon: '⊕', color: 'var(--blue-b)'  },
    unreleased:  { label: 'NOT YET',    cls: 'coord-card-dim',    icon: '○', color: 'var(--dim2)'    },
  }
  const s = statusMap[coord.status]

  return (
    <div className={`coord-card ${s.cls}`} onClick={onTap}>
      <div style={{ fontFamily: 'var(--font-b)', fontSize: '1.2rem', color: s.color, flexShrink: 0, width: 28, textAlign: 'center' }}>{s.icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.2em', color: 'var(--dim2)', marginBottom: '.2rem' }}>
          COORD-{coord.id} · {coord.slug}
        </div>
        <div style={{ fontFamily: 'var(--font-b)', fontSize: '1rem', letterSpacing: '.06em', color: 'var(--fg)' }}>{coord.name}</div>
      </div>
      <div style={{ fontFamily: 'var(--font-m)', fontSize: '.4rem', letterSpacing: '.18em', color: s.color, flexShrink: 0 }}>{s.label}</div>
    </div>
  )
}

// ─── SIGNAL COORD DETAIL ──────────────────────────────────────────────────────
function SignalScreen() {
  const [freq, setFreq]   = useState(137.0)
  const [locked, setLocked] = useState(false)
  const [bars, setBars]   = useState<number[]>(Array(24).fill(0))
  const TARGET = 440.7

  useEffect(() => {
    let id: number
    const animate = () => {
      setBars(prev => prev.map(() => locked ? 0.5 + Math.random() * 0.5 : Math.random()))
      id = requestAnimationFrame(animate)
    }
    id = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(id)
  }, [locked])

  const diff   = Math.abs(freq - TARGET)
  const signal = Math.max(0, 1 - diff / 150)

  const tune = (delta: number) => {
    setFreq(f => {
      const next = Math.round((f + delta) * 10) / 10
      if (Math.abs(next - TARGET) < 0.4) setLocked(true)
      return next
    })
  }

  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      <div style={{ padding: '1.5rem 1.25rem' }}>
        <div className="label" style={{ marginBottom: '.5rem' }}>COORD-04</div>
        <div style={{ fontFamily: 'var(--font-b)', fontSize: '2rem', letterSpacing: '.06em', color: 'var(--fg)', marginBottom: '2rem' }}>THE SIGNAL</div>

        <div style={{
          border: `1px solid ${locked ? 'var(--green)' : 'var(--border)'}`,
          background: 'var(--bg)', padding: '1.5rem 1rem', marginBottom: '1.5rem',
          boxShadow: locked ? 'var(--glow-g)' : 'none', transition: 'all .5s',
        }}>
          <div style={{ display: 'flex', gap: 2, alignItems: 'flex-end', height: 64, justifyContent: 'center' }}>
            {bars.map((h, i) => (
              <div key={i} style={{
                flex: 1, height: `${(locked ? 0.3 + h * 0.7 : h) * 100}%`,
                background: locked ? `rgba(90,173,101,${0.4 + h * 0.6})` : `rgba(90,90,80,${0.3 + h * 0.4})`,
                transition: 'height .05s, background .3s', minHeight: 2,
              }} />
            ))}
          </div>
          <div style={{
            textAlign: 'center', marginTop: '1rem',
            fontFamily: 'var(--font-b)', fontSize: '2.2rem',
            color: locked ? 'var(--green-b)' : 'var(--fg)', letterSpacing: '.05em',
            textShadow: locked ? '0 0 20px rgba(90,173,101,.5)' : 'none', transition: 'all .3s',
          }}>
            {freq.toFixed(1)} <span style={{ fontSize: '.8rem', color: 'var(--dim)' }}>MHz</span>
          </div>
          <div style={{ height: 2, background: 'var(--border)', marginTop: '1rem' }}>
            <div style={{
              height: '100%', width: `${signal * 100}%`,
              background: locked ? 'var(--green-b)' : 'var(--dim)',
              transition: 'width .2s, background .3s',
              boxShadow: locked ? 'var(--glow-g)' : 'none',
            }} />
          </div>
        </div>

        {locked ? (
          <div style={{
            textAlign: 'center', padding: '1.5rem',
            border: '1px solid var(--green)', background: 'var(--green-d)',
            boxShadow: 'var(--glow-g)', animation: 'fadeUp .4s ease',
          }}>
            <div style={{ fontFamily: 'var(--font-b)', fontSize: '1.4rem', color: 'var(--green-b)', letterSpacing: '.08em', marginBottom: '.5rem' }}>
              FREQUENCY LOCKED
            </div>
            <div style={{ fontFamily: 'var(--font-t)', fontSize: '.7rem', color: 'var(--dim)', fontStyle: 'italic' }}>
              The signal was always there. You just had to listen.
            </div>
            <div style={{ fontFamily: 'var(--font-b)', fontSize: '1.6rem', color: 'var(--amber)', marginTop: '1rem', letterSpacing: '.1em' }}>G</div>
            <div className="label" style={{ marginTop: '.25rem' }}>CIPHER FRAGMENT REVEALED</div>
            <a href="/cold-code/respect-the-lobby" style={{
              display: 'inline-block', marginTop: '1rem',
              fontFamily: 'var(--font-m)', fontSize: '.44rem',
              letterSpacing: '.18em', color: 'var(--green-b)', textDecoration: 'none', textTransform: 'uppercase',
            }}>READ ARTICLE VI ON SITE →</a>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 1, background: 'var(--border)' }}>
            {[[-0.1, '← –0.1 MHz'], [0.1, '+0.1 MHz →'], [-1, '← –1.0 MHz'], [1, '+1.0 MHz →']].map(([d, label]) => (
              <button key={String(label)} className="btn" onClick={() => tune(Number(d))}
                style={{ width: '100%', padding: '1rem', fontSize: '.55rem' }}>
                {label}
              </button>
            ))}
          </div>
        )}

        <div style={{ fontFamily: 'var(--font-t)', fontSize: '.62rem', color: 'var(--dim)', marginTop: '1.5rem', lineHeight: 1.7, fontStyle: 'italic' }}>
          "They said the frequency was abandoned. They were wrong. It was waiting."
        </div>
      </div>
    </div>
  )
}

// ─── LORE SCREEN ──────────────────────────────────────────────────────────────
function LoreScreen({ userRank }: { userRank: string }) {
  const [open, setOpen] = useState<string | null>(null)
  const RANK_ORDER = ['prospect', 'family-friend', 'associate', 'lieutenant', 'capo', 'don', 'boss', 'ghost', 'curator', 'cartel']

  const hasAccess = (requiredRank: string | null) => {
    if (!requiredRank) return true
    return RANK_ORDER.indexOf(userRank.toLowerCase()) >= RANK_ORDER.indexOf(requiredRank.toLowerCase())
  }

  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      <div style={{ padding: '1.25rem 1.25rem .75rem' }}>
        <div className="label" style={{ marginBottom: '.3rem' }}>// THE LORE</div>
        <div style={{ fontFamily: 'var(--font-t)', fontSize: '.62rem', color: 'var(--dim)', fontStyle: 'italic' }}>
          The mythology of Cold Empire. Read carefully.
        </div>
      </div>
      <hr className="rule" />
      {CHAPTERS.map(ch => {
        const isLocked = !hasAccess(ch.rank)
        const isOpen   = open === ch.num
        return (
          <div key={ch.num}
            onClick={() => !isLocked && setOpen(isOpen ? null : ch.num)}
            style={{
              padding: '1rem 1.25rem', borderBottom: '1px solid var(--border)',
              cursor: isLocked ? 'default' : 'pointer',
              opacity: isLocked ? .45 : 1,
              background: isOpen ? 'var(--bg2)' : 'var(--bg)', transition: 'background .15s',
            }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: 'var(--font-m)', fontSize: '.4rem', letterSpacing: '.2em', color: 'var(--dim2)', marginBottom: '.3rem' }}>CHAPTER {ch.num}</div>
                <div style={{ fontFamily: 'var(--font-b)', fontSize: '.95rem', letterSpacing: '.05em', color: isLocked ? 'var(--dim)' : 'var(--fg)' }}>{ch.title}</div>
              </div>
              {isLocked
                ? <div className="label" style={{ color: 'var(--dim2)', fontSize: '.36rem' }}>⊘ {ch.rank?.toUpperCase()}+</div>
                : <div style={{ color: 'var(--dim)', fontSize: '.7rem' }}>{isOpen ? '▲' : '▼'}</div>}
            </div>
            {ch.teaser && isLocked && (
              <div style={{ fontFamily: 'var(--font-t)', fontSize: '.55rem', color: 'var(--dim2)', fontStyle: 'italic', marginTop: '.5rem' }}>"{ch.teaser}"</div>
            )}
            {isOpen && (
              <div style={{ marginTop: '1rem', animation: 'fadeUp .3s ease' }}>
                <div style={{ fontFamily: 'var(--font-s)', fontSize: '.9rem', lineHeight: 1.85, color: 'var(--fg)', opacity: .88 }}>
                  There is no beginning that is not also an end. Cold understood this before he built anything. The name came first — not as a brand, not as a symbol, but as a feeling. The cold clarity of knowing exactly who you are and exactly who you are not.
                  <br /><br />
                  Every family has a founding story. This one starts with a number: 13. Then another: 7. The space between them is everything.
                </div>
                <a href={`/cold-code/${ch.siteSlug}`} style={{
                  display: 'inline-block', marginTop: '1rem',
                  fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em',
                  color: 'var(--green-b)', textDecoration: 'none', textTransform: 'uppercase',
                }}>READ FULL ARTICLE ON SITE →</a>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

// ─── IB6 SCREEN ───────────────────────────────────────────────────────────────
function Ib6Screen() {
  const seats = [
    { num: '01', callsign: 'PHANTOM',   rank: 'CARTEL',  founding: true,  status: 'confirmed' },
    { num: '07', callsign: 'NIGHTHAWK', rank: 'GHOST',   founding: true,  status: 'confirmed' },
    { num: '12', callsign: 'REVOLVER',  rank: 'CURATOR', founding: true,  status: 'confirmed' },
    { num: '—',  callsign: 'OPEN SEAT', rank: null,      founding: false, status: 'open'      },
    { num: '—',  callsign: 'OPEN SEAT', rank: null,      founding: false, status: 'open'      },
    { num: '—',  callsign: 'OPEN SEAT', rank: null,      founding: false, status: 'open'      },
  ]

  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      <div style={{
        padding: '1.5rem 1.25rem', background: 'var(--blue-d)',
        borderBottom: '1px solid var(--blue)', position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', right: '-2rem', top: '-1rem',
          fontFamily: 'var(--font-b)', fontSize: '8rem',
          color: 'rgba(42,74,107,.15)', lineHeight: 1, pointerEvents: 'none',
        }}>IB6</div>
        <div className="label label-blue" style={{ marginBottom: '.4rem' }}>ILLEGAL BACKROOM SIX</div>
        <div style={{ fontFamily: 'var(--font-b)', fontSize: '1.8rem', letterSpacing: '.06em', color: 'var(--blue-b)', marginBottom: '.75rem' }}>SESSION 009</div>
        <div style={{
          display: 'flex', alignItems: 'center', gap: '.75rem',
          padding: '.6rem 1rem', border: '1px solid var(--border)', background: 'var(--bg)', width: 'fit-content',
        }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--dim)', display: 'inline-block' }} />
          <span style={{ fontFamily: 'var(--font-m)', fontSize: '.48rem', letterSpacing: '.18em', color: 'var(--dim)' }}>NEXT SESSION · TBA</span>
        </div>
      </div>

      <div style={{ padding: '.75rem 1.25rem .5rem' }}>
        <div className="label" style={{ marginBottom: '.75rem' }}>// TABLE SEATS</div>
      </div>
      {seats.map((s, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center',
          padding: '.85rem 1.25rem', borderBottom: '1px solid var(--border)',
          background: s.status === 'open' ? 'var(--bg)' : 'var(--bg2)', gap: '1rem',
        }}>
          <div style={{ fontFamily: 'var(--font-b)', fontSize: '1.1rem', color: s.founding ? 'var(--amber)' : 'var(--dim2)', width: 28, flexShrink: 0 }}>
            {s.founding ? `◆${s.num}` : '○'}
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontFamily: 'var(--font-b)', fontSize: '.9rem', letterSpacing: '.05em', color: s.status === 'open' ? 'var(--dim2)' : 'var(--fg)' }}>{s.callsign}</div>
            {s.rank && <div className="label" style={{ fontSize: '.38rem', marginTop: '.2rem' }}>{s.rank}</div>}
          </div>
          <div className={`label ${s.status === 'confirmed' ? 'label-green' : ''}`} style={{ fontSize: '.38rem', color: s.status === 'open' ? 'var(--dim2)' : undefined }}>
            {s.status.toUpperCase()}
          </div>
        </div>
      ))}

      <div style={{ padding: '1.25rem', borderTop: '1px solid var(--border)', marginTop: 1 }}>
        <div style={{ fontFamily: 'var(--font-t)', fontSize: '.65rem', color: 'var(--dim)', lineHeight: 1.7, fontStyle: 'italic', marginBottom: '1rem' }}>
          "Six seats. No cameras. No record. What happens at the table stays at the table."
        </div>
        <a href="/ib6" style={{
          fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em',
          color: 'var(--blue-b)', textDecoration: 'none', textTransform: 'uppercase',
        }}>◆ IB6 FULL PAGE →</a>
      </div>
    </div>
  )
}

// ─── RECORD SCREEN ────────────────────────────────────────────────────────────
interface RecordProps { callsign: string; rank: string; points: number; email: string }

function RecordScreen({ callsign, rank, points, email }: RecordProps) {
  const stats = [
    { label: 'RANK',            val: rank.toUpperCase(),         color: 'var(--fg)'     },
    { label: 'EMAIL',           val: email,                      color: 'var(--dim)'    },
    { label: 'POINTS',          val: points.toLocaleString(),    color: 'var(--green-b)' },
    { label: 'CIPHER STATUS',   val: '2/7 FOUND',                color: 'var(--green-b)' },
    { label: 'COLD\'S STITCH',  val: '◆ LOGGED',                 color: 'var(--green-b)' },
    { label: 'LID LORE LINE',   val: '"The cold was already in you."', color: 'var(--dim)', italic: true },
    { label: 'WALLET',          val: 'NOT CONNECTED',            color: 'var(--dim)'    },
    { label: 'SOULBOUND TOKEN', val: '— PENDING CONNECT',        color: 'var(--dim)'    },
  ]

  return (
    <div className="screen-scroll" style={{ paddingBottom: 'calc(var(--nav-h) + 1rem)' }}>
      <div style={{
        background: 'var(--amber-dim)', borderBottom: '1px solid var(--amber-d)',
        padding: '1.5rem 1.25rem', position: 'relative', overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', right: '-1rem', top: '-1rem',
          fontFamily: 'var(--font-b)', fontSize: '7rem',
          color: 'rgba(200,168,64,.05)', lineHeight: 1, pointerEvents: 'none',
        }}>◈</div>
        <div className="label label-amber" style={{ marginBottom: '.4rem' }}>FOUNDING SEAT · SERIES 001</div>
        <div style={{
          fontFamily: 'var(--font-b)', fontSize: '2.2rem', color: 'var(--amber)',
          letterSpacing: '.06em', textShadow: '0 0 25px rgba(200,168,64,.3)',
        }}>{callsign}</div>
        <div style={{ fontFamily: 'var(--font-m)', fontSize: '.48rem', letterSpacing: '.18em', color: 'var(--amber-d)', marginTop: '.4rem' }}>
          {rank.toUpperCase()}
        </div>
      </div>

      {stats.map((s, i) => (
        <div key={i} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '.9rem 1.25rem', borderBottom: '1px solid var(--border)',
          background: i % 2 === 0 ? 'var(--bg)' : 'var(--bg2)',
        }}>
          <div className="label">{s.label}</div>
          <div style={{
            fontFamily: s.italic ? 'var(--font-t)' : 'var(--font-m)', fontSize: '.55rem',
            letterSpacing: '.1em', color: s.color, fontStyle: s.italic ? 'italic' : 'normal',
            maxWidth: '60%', textAlign: 'right',
          }}>{s.val}</div>
        </div>
      ))}

      <div style={{ padding: '1.25rem' }}>
        <a href="/portal" style={{
          display: 'block', width: '100%', padding: '.85rem', fontSize: '.55rem',
          fontFamily: 'var(--font-m)', letterSpacing: '.18em', textTransform: 'uppercase',
          border: '1px solid var(--amber-d)', color: 'var(--amber)',
          background: 'none', textDecoration: 'none', textAlign: 'center',
          boxShadow: 'var(--glow-a)',
        }}>◆ FULL PORTAL →</a>
        <div style={{ fontFamily: 'var(--font-t)', fontSize: '.56rem', color: 'var(--dim)', textAlign: 'center', marginTop: '.75rem', fontStyle: 'italic' }}>
          Your intake is for Cold's eyes only.
        </div>
      </div>

      <div style={{ margin: '0 1.25rem 1.25rem', border: '1px solid var(--border)', padding: '1rem', background: 'var(--bg2)' }}>
        <div className="label" style={{ marginBottom: '.5rem' }}>CUFF WORD POOL</div>
        <div style={{ fontFamily: 'var(--font-m)', fontSize: '.55rem', color: 'var(--dim)', lineHeight: 1.6 }}>
          3 of 25 founding members have compared words.<br />
          Compare yours to activate the cipher event.
        </div>
        <button className="btn btn-green" style={{ marginTop: '.75rem', fontSize: '.48rem' }}>
          COMPARE CUFF WORD
        </button>
      </div>
    </div>
  )
}

// ─── COORD OVERLAY ────────────────────────────────────────────────────────────
function CoordOverlay({ coord, onBack }: { coord: typeof COORDINATES[number]; onBack: () => void }) {
  return (
    <div style={{ position: 'fixed', inset: 0, background: 'var(--bg)', zIndex: 300, display: 'flex', flexDirection: 'column' }}>
      <div style={{
        height: 48, borderBottom: '1px solid var(--border)',
        display: 'flex', alignItems: 'center', padding: '0 1.25rem', gap: '1rem', flexShrink: 0,
      }}>
        <button className="btn" onClick={onBack} style={{ fontSize: '.44rem', padding: '.35rem .75rem' }}>← BACK</button>
        <div className="label">COORD-{coord.id} · {coord.slug}</div>
      </div>
      {coord.id === '04' ? <SignalScreen /> : (
        <div style={{
          flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexDirection: 'column', gap: '1rem', padding: '2rem',
        }}>
          <div style={{ fontFamily: 'var(--font-b)', fontSize: '2rem', color: 'var(--fg)', letterSpacing: '.06em' }}>{coord.name}</div>
          <div style={{ fontFamily: 'var(--font-t)', fontSize: '.7rem', color: 'var(--dim)', fontStyle: 'italic', textAlign: 'center' }}>
            This coordinate is active in the field.<br />Check the site for the full experience.
          </div>
          <a href="/cold-code" style={{
            fontFamily: 'var(--font-m)', fontSize: '.44rem', letterSpacing: '.18em',
            color: 'var(--green-b)', textDecoration: 'none', textTransform: 'uppercase', marginTop: '.5rem',
          }}>READ THE COLD CODE →</a>
        </div>
      )}
    </div>
  )
}

// ─── NOT LOGGED IN STATE ──────────────────────────────────────────────────────
function NotAuthScreen() {
  return (
    <div style={{
      position: 'fixed', inset: 0, background: 'var(--bg)',
      display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
      justifyContent: 'center', padding: '2.5rem', zIndex: 100,
    }}>
      <div className="label label-amber" style={{ marginBottom: '1rem' }}>ACCESS REQUIRED</div>
      <div style={{ fontFamily: 'var(--font-b)', fontSize: 'clamp(1.8rem,6vw,2.4rem)', color: 'var(--fg)', letterSpacing: '.05em', marginBottom: '1rem' }}>
        MEMBERS ONLY
      </div>
      <p style={{ fontFamily: 'var(--font-t)', fontSize: '.72rem', color: 'var(--dim)', fontStyle: 'italic', lineHeight: 1.7, marginBottom: '2rem', maxWidth: 340 }}>
        The companion app is for registered members of the Cold Empire. Create an account or log in to continue.
      </p>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <a href="/auth/login" className="btn btn-green" style={{ fontSize: '.65rem', padding: '.75rem 2rem', letterSpacing: '.22em', textDecoration: 'none' }}>
          ◆ LOG IN
        </a>
        <a href="/auth/register" className="btn" style={{ fontSize: '.65rem', padding: '.75rem 2rem', letterSpacing: '.22em', textDecoration: 'none' }}>
          CREATE ACCOUNT
        </a>
      </div>
    </div>
  )
}

// ─── ROOT APP ─────────────────────────────────────────────────────────────────
export default function CompanionPage() {
  const { data: session, status } = useSession()
  const [phase, setPhase]   = useState<'intercept' | 'app'>('intercept')
  const [screen, setScreen] = useState('home')
  const [coordOverlay, setCoord] = useState<typeof COORDINATES[number] | null>(null)

  const enterApp = useCallback(() => setPhase('app'), [])

  // Inject Google Fonts
  useEffect(() => {
    const link = document.createElement('link')
    link.rel  = 'stylesheet'
    link.href = FONTS_URL
    document.head.appendChild(link)
    return () => { document.head.removeChild(link) }
  }, [])

  // Derive member data from session
  const user = session?.user as { name?: string; email?: string; rank?: string; points?: number } | undefined
  const callsign    = user?.name?.toUpperCase() ?? 'OPERATIVE'
  const rank        = user?.rank ?? 'prospect'
  const points      = user?.points ?? 0
  const coordsFound = 3 // TODO: derive from mission completions
  const email       = user?.email ?? '—'

  const screenLabel: Record<string, string> = {
    home:   'HOME',
    arg:    'MISSION CONTROL',
    lore:   'THE LORE',
    ib6:    'IB6 · SESSION 009',
    record: 'THE RECORD',
  }

  return (
    <>
      <style>{GLOBAL_CSS}</style>
      <div className="capp">
        <div className="sweep-line" />

        {status === 'loading' && (
          <div style={{ position: 'fixed', inset: 0, background: 'var(--bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 200 }}>
            <span style={{ fontFamily: 'var(--font-m)', fontSize: '.55rem', letterSpacing: '.2em', color: 'var(--dim)' }}>AUTHENTICATING...</span>
          </div>
        )}

        {status === 'unauthenticated' && <NotAuthScreen />}

        {status === 'authenticated' && phase === 'intercept' && <InterceptScreen onEnter={enterApp} />}

        {status === 'authenticated' && phase === 'app' && (
          <div style={{
            display: 'flex', flexDirection: 'column',
            height: '100vh', width: '100%',
            maxWidth: 430, margin: '0 auto',
            background: 'var(--bg)', boxShadow: '0 0 80px rgba(0,0,0,.8)',
          }}>
            <TopBar screen={screenLabel[screen] ?? screen.toUpperCase()} />

            <div style={{ flex: 1, overflow: 'hidden', position: 'relative' }}>
              {screen === 'home'   && <HomeScreen callsign={callsign} rank={rank} coordsFound={coordsFound} points={points} />}
              {screen === 'arg'    && <ArgScreen  coordsFound={coordsFound} onCoordTap={setCoord} />}
              {screen === 'lore'   && <LoreScreen userRank={rank} />}
              {screen === 'ib6'    && <Ib6Screen  />}
              {screen === 'record' && <RecordScreen callsign={callsign} rank={rank} points={points} email={email} />}
            </div>

            <BottomNav active={screen} onNav={setScreen} />

            {coordOverlay && (
              <CoordOverlay coord={coordOverlay} onBack={() => setCoord(null)} />
            )}
          </div>
        )}
      </div>
    </>
  )
}
