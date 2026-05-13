import { getArticleBySlug, getAdjacentArticles, coldCodeArticles } from '@/data/coldCode'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import EmailCapture from '@/components/ui/EmailCapture'

export function generateStaticParams() {
  return coldCodeArticles.map((a) => ({ article: a.slug }))
}

export default function ArticlePage({ params }: { params: { article: string } }) {
  const article = getArticleBySlug(params.article)
  if (!article) notFound()

  const { prev, next } = getAdjacentArticles(article.id)

  const sections = [
    { label: 'The Rule', content: article.rule },
    { label: 'What It Means', content: article.meaning },
    { label: 'What It Looks Like', content: article.looksLike },
    { label: 'What Breaks It', content: article.breaksIt },
    { label: 'Why It Matters', content: article.whyItMatters },
  ]

  return (
    <div className="min-h-screen bg-cold-black">
      <div className="max-w-6xl mx-auto px-6 lg:px-16 py-16">
        <div className="flex flex-col lg:flex-row gap-12">
          {/* Main */}
          <div className="flex-1">
            {/* Breadcrumb */}
            <div className="flex items-center gap-2 mb-8 text-cold-smoke font-mono text-xs">
              <Link href="/cold-code" className="hover:text-cold-green transition-colors">Cold Code</Link>
              <span>/</span>
              <span className="text-cold-white">Article {article.id}</span>
            </div>

            {/* Title */}
            <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">
              ARTICLE {article.id} OF 13
            </p>
            <h1 className="text-3xl lg:text-4xl font-mono text-cold-white mb-4">{article.shortTitle}</h1>
            <p className="text-cold-smoke font-mono text-lg mb-12 leading-relaxed">{article.teaser}</p>

            {/* Rule highlight */}
            <div className="border-l-2 border-cold-green pl-6 mb-12">
              <p className="text-cold-green font-mono text-xl">&ldquo;{article.rule}&rdquo;</p>
            </div>

            {/* Sections */}
            <div className="space-y-10">
              {sections.map((s) => (
                <div key={s.label}>
                  <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-3">{s.label}</p>
                  <p className="text-cold-white font-mono text-sm leading-relaxed">{s.content}</p>
                </div>
              ))}
            </div>

            {/* Nav */}
            <div className="flex items-center justify-between mt-16 pt-8 border-t border-cold-gray/40">
              {prev ? (
                <Link href={`/cold-code/${prev.slug}`} className="group flex items-center gap-3 text-cold-smoke hover:text-cold-green transition-colors">
                  <span>←</span>
                  <div>
                    <p className="font-mono text-xs tracking-widest uppercase">Previous</p>
                    <p className="font-mono text-sm group-hover:text-cold-green">{prev.shortTitle}</p>
                  </div>
                </Link>
              ) : <div />}

              {next ? (
                <Link href={`/cold-code/${next.slug}`} className="group flex items-center gap-3 text-right text-cold-smoke hover:text-cold-green transition-colors">
                  <div>
                    <p className="font-mono text-xs tracking-widest uppercase">Next</p>
                    <p className="font-mono text-sm group-hover:text-cold-green">{next.shortTitle}</p>
                  </div>
                  <span>→</span>
                </Link>
              ) : <div />}
            </div>

            {/* Email */}
            <div className="mt-12 pt-8 border-t border-cold-gray/40">
              <p className="text-cold-smoke font-mono text-sm mb-4">Want the next signal?</p>
              <EmailCapture source={`cold-code-${article.slug}`} tags="lore,code" />
            </div>
          </div>

          {/* Sidebar */}
          <aside className="lg:w-64 flex-shrink-0 space-y-6">
            <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
              <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Related Mission</p>
              <p className="text-cold-white font-mono text-sm">{article.relatedMission}</p>
              <Link href="/portal/missions" className="block mt-3 text-cold-green font-mono text-xs tracking-wide hover:opacity-70 transition-opacity">
                View Missions →
              </Link>
            </div>

            <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
              <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Related Drop</p>
              <p className="text-cold-white font-mono text-sm">{article.relatedProduct}</p>
              <Link href="/store" className="block mt-3 text-cold-green font-mono text-xs tracking-wide hover:opacity-70 transition-opacity">
                Shop the Drop →
              </Link>
            </div>

            <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
              <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">Related Rank</p>
              <p className="text-cold-white font-mono text-sm">{article.relatedRank}</p>
              <Link href="/cartel" className="block mt-3 text-cold-green font-mono text-xs tracking-wide hover:opacity-70 transition-opacity">
                View Ranks →
              </Link>
            </div>

            <div className="border border-cold-gray/40 bg-cold-charcoal p-5">
              <p className="text-xs tracking-widest uppercase text-cold-smoke font-mono mb-4">All Articles</p>
              <div className="space-y-2">
                {coldCodeArticles.map((a) => (
                  <Link
                    key={a.slug}
                    href={`/cold-code/${a.slug}`}
                    className={`block font-mono text-xs py-1 transition-colors ${a.slug === params.article ? 'text-cold-green' : 'text-cold-smoke hover:text-cold-white'}`}
                  >
                    {a.id}. {a.shortTitle}
                  </Link>
                ))}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  )
}
