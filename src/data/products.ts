export interface Product {
  id: string
  slug: string
  name: string
  price: number
  description: string
  loreNote: string
  collection: string
  tags: string[]
  images: string[]
  sizes: string[]
  colors: string[]
  inStock: boolean
  featured: boolean
  stripePriceId?: string
}

export const products: Product[] = [
  {
    id: 'prod_001',
    slug: 'find-the-door-hoodie',
    name: 'Find the Door Hoodie',
    price: 8500,
    description:
      'Heavy black pullover hoodie. Minimal branding. A quiet signal for the ones who know where to look.',
    loreNote:
      'This is not merch. This is a marker. Wear it and someone will ask. That\'s when you decide if they deserve the answer.',
    collection: 'Find the Door',
    tags: ['hoodie', 'ccc', 'featured'],
    images: ['/images/products/door-hoodie-1.jpg'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    colors: ['Black'],
    inStock: true,
    featured: true,
  },
  {
    id: 'prod_002',
    slug: 'stay-cold-hoodie',
    name: 'Stay Cold Hoodie',
    price: 8500,
    description:
      'Heavyweight cold-weather hoodie. Cold Empire emblem. For the ones who stay cold when it matters.',
    loreNote:
      'Article XIII. When things get hot, stay cold. Wear the reminder.',
    collection: 'Cold Code',
    tags: ['hoodie', 'ccc', 'featured', 'cartel'],
    images: ['/images/products/stay-cold-hoodie-1.jpg'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    colors: ['Black'],
    inStock: true,
    featured: true,
  },
  {
    id: 'prod_003',
    slug: 'cold-signal-tee',
    name: 'Cold Signal Tee',
    price: 4500,
    description: 'Black on black. Slim fit. The signal is there if you know what to look for.',
    loreNote:
      'Some people wear logos. Some people wear signals. This is the difference.',
    collection: 'Wear the Signal',
    tags: ['tee', 'ccc', 'featured'],
    images: ['/images/products/signal-tee-1.jpg'],
    sizes: ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
    colors: ['Black', 'Charcoal'],
    inStock: true,
    featured: true,
  },
  {
    id: 'prod_004',
    slug: 'ib6-lobby-hoodie',
    name: 'IB6 Lobby Hoodie',
    price: 7500,
    description: 'For the stoner gamer who lives in the lobby. Heavy. Dark. Comfortable.',
    loreNote:
      'The lobby opens when you step in. This is the uniform.',
    collection: 'IB6 Lobby',
    tags: ['hoodie', 'ib6', 'gaming'],
    images: ['/images/products/ib6-hoodie-1.jpg'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    colors: ['Black'],
    inStock: true,
    featured: false,
  },
  {
    id: 'prod_005',
    slug: 'cartel-blackout-hat',
    name: 'Cartel Blackout Hat',
    price: 3500,
    description: 'Structured black cap. Cold Cartel emblem. Members only energy.',
    loreNote:
      'Before rank comes code. This hat is worn by people who read it.',
    collection: 'Cartel Blackout',
    tags: ['hat', 'cartel', 'ccc'],
    images: ['/images/products/cartel-hat-1.jpg'],
    sizes: ['One Size'],
    colors: ['Black'],
    inStock: true,
    featured: false,
  },
  {
    id: 'prod_006',
    slug: 'cold-empire-flag',
    name: 'Cold Empire Flag',
    price: 2500,
    description: 'Black on black. 3x5. Claim the territory.',
    loreNote:
      'Article X. Everywhere the flag appears, the empire has territory.',
    collection: 'Cartel Blackout',
    tags: ['accessories', 'cartel', 'ccc'],
    images: ['/images/products/ce-flag-1.jpg'],
    sizes: ['3x5 ft'],
    colors: ['Black'],
    inStock: true,
    featured: false,
  },
  {
    id: 'prod_007',
    slug: 'no-fake-smoke-sticker-pack',
    name: 'No Fake Smoke Sticker Pack',
    price: 1200,
    description: '5 stickers. Cold Empire icons. Go put the signal somewhere it will be found.',
    loreNote:
      'Article V. Every sticker is a door someone might find.',
    collection: 'Find the Door',
    tags: ['stickers', 'ccc', 'ib6'],
    images: ['/images/products/sticker-pack-1.jpg'],
    sizes: ['Pack of 5'],
    colors: ['Mixed'],
    inStock: true,
    featured: false,
  },
  {
    id: 'prod_008',
    slug: 'move-quiet-tee',
    name: 'Move Quiet Tee',
    price: 4500,
    description: 'Minimal. Intentional. Article XI in wearable form.',
    loreNote:
      'Announce nothing. Deliver everything. Let the arrival speak.',
    collection: 'Cold Code',
    tags: ['tee', 'ccc', 'cartel'],
    images: ['/images/products/move-quiet-tee-1.jpg'],
    sizes: ['S', 'M', 'L', 'XL', 'XXL'],
    colors: ['Black'],
    inStock: true,
    featured: false,
  },
]

export function getProductBySlug(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug)
}

export function getProductsByTag(tag: string): Product[] {
  return products.filter((p) => p.tags.includes(tag))
}

export function getFeaturedProducts(): Product[] {
  return products.filter((p) => p.featured && p.inStock)
}

export function getCollections(): string[] {
  return Array.from(new Set(products.map((p) => p.collection)))
}

export function getProductsByCollection(collection: string): Product[] {
  return products.filter((p) => p.collection === collection)
}

export function formatPrice(cents: number): string {
  return `$${(cents / 100).toFixed(2)}`
}
