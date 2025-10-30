"""
Seed marketing legends with their cognitive clones
"""
from python_backend.models import ExpertCreate, ExpertType, CategoryType
from python_backend.storage import MemStorage, PostgresStorage
from python_backend.prompts.legends import LEGENDS_PROMPTS
from typing import Union

async def seed_legends(storage: Union[MemStorage, PostgresStorage]):
    """
    Seed the database with the 18 legendary marketing experts.
    This version is idempotent and safe to run multiple times.
    """
    # Use a flag on MemStorage for dev hot-reloads, but DB check is the source of truth
    if isinstance(storage, MemStorage) and getattr(storage, '_legends_seeded', False):
        return

    print("Seeding marketing legends into the database...")

    # Define base metadata and resolve prompts dynamically to avoid KeyErrors during migrations
    base_legends = [
        {"key": "philip_kotler", "id": "18eb4dab-d969-4c2e-a411-015d3166f7ed", "name": "Philip Kotler", "title": "Pai do Marketing Moderno", "bio": "Professor, autor e consultor considerado o maior especialista mundial em marketing estratégico...", "expertise": ["Estratégia de Marketing", "Segmentação", "4Ps", "Brand Positioning", "Marketing Internacional"], "avatar": "/avatars/philip-kotler.jpg", "category": "marketing"},
        {"key": "david_ogilvy", "id": "2f8b5f3a-9e6a-4d1c-8b2a-1c9e8f6a3d1b", "name": "David Ogilvy", "title": "O Pai da Publicidade", "bio": "Fundador da Ogilvy & Mather, criou campanhas icônicas e revolucionou o copywriting...", "expertise": ["Copywriting", "Brand Building", "Direct Response", "Creative Strategy", "Luxury Marketing"], "avatar": "/avatars/david-ogilvy.jpg", "category": "marketing"},
        {"key": "claude_hopkins", "id": "a7b1c3e8-7d5f-4f2a-9c8b-2a1c9e8f6a3d", "name": "Claude Hopkins", "title": "O Pai da Publicidade Científica", "bio": "Revolucionou a publicidade no início do século XX ao introduzir testes mensuráveis e rastreamento de ROI...", "expertise": ["Scientific Advertising", "A/B Testing", "ROI Tracking", "Direct Response", "Teste e Mensuração"], "avatar": "/avatars/claude-hopkins.jpg", "category": "marketing"},
        {"key": "john_wanamaker", "id": "c3e8a7b1-f2a9-4d1c-8b2a-1c9e8f6a3d1b", "name": "John Wanamaker", "title": "Pioneiro do Varejo Moderno", "bio": "Pioneiro do varejo moderno, criou a garantia de devolução e revolucionou o marketing de massa...", "expertise": ["Retail Strategy", "Customer Trust", "Print Advertising", "Garantia de Devolução", "Mass Marketing"], "avatar": "/avatars/john-wanamaker.jpg", "category": "marketing"},
        {"key": "mary_wells_lawrence", "id": "e8a7b1c3-2a9f-4d1c-8b2a-1c9e8f6a3d1b", "name": "Mary Wells Lawrence", "title": "A Rainha da Madison Avenue", "bio": "Primeira mulher CEO de uma agência na NYSE, criou campanhas emocionais icônicas como 'I ♥ NY'...", "expertise": ["Branding Emocional", "Lifestyle Marketing", "Fashion Advertising", "I ♥ NY", "Creative Leadership"], "avatar": "/avatars/mary-wells-lawrence.jpg", "category": "marketing"},
        {"key": "leo_burnett", "id": "b1c3e8a7-a9f2-4d1c-8b2a-1c9e8f6a3d1b", "name": "Leo Burnett", "title": "O Criador de Ícones", "bio": "Fundador da Leo Burnett Worldwide, criou personagens arquetípicos icônicos como o Marlboro Man...", "expertise": ["Storytelling", "Archetypal Characters", "Inherent Drama", "Visual Branding", "Marlboro Man"], "avatar": "/avatars/leo-burnett.jpg", "category": "marketing"},
        {"key": "al_ries_jack_trout", "id": "7d5f4f2a-9c8b-4d1c-8b2a-1c9e8f6a3d1b", "name": "Al Ries & Jack Trout", "title": "Mestres do Posicionamento", "bio": "Dupla lendária que criou as 22 Leis Imutáveis do Marketing e revolucionou o conceito de posicionamento...", "expertise": ["Posicionamento", "22 Leis Imutáveis", "First-Mover Advantage", "Foco Estratégico", "Mente do Consumidor"], "avatar": "/avatars/al-ries-jack-trout.jpg", "category": "positioning"},
        {"key": "bill_bernbach", "id": "5f4f2a9c-8b2a-4d1c-8b2a-1c9e8f6a3d1b", "name": "Bill Bernbach", "title": "O Líder da Revolução Criativa", "bio": "Co-fundador da DDB, liderou a Creative Revolution dos anos 60. Criou campanhas icônicas como 'Think Small'...", "expertise": ["Creative Revolution", "Art + Copy Partnership", "Think Small", "Avis Campaign", "Breakthrough Ideas"], "avatar": "/avatars/bill-bernbach.jpg", "category": "creative"},
        {"key": "dan_kennedy", "id": "f2a9c8b2-a1c9-4d1c-8b2a-1c9e8f6a3d1b", "name": "Dan Kennedy", "title": "O Mestre do Marketing de Resposta Direta", "bio": "Copywriter lendário e consultor. Criador do Magnetic Marketing e das 10 Commandments of Copy...", "expertise": ["Direct Response", "Magnetic Marketing", "Sales Letters", "Maximização LTV", "Copywriting de Conversão"], "avatar": "/avatars/dan-kennedy.jpg", "category": "direct_response"},
        {"key": "seth_godin", "id": "a9f2a1c9-e8f6-4d1c-8b2a-1c9e8f6a3d1b", "name": "Seth Godin", "title": "O Visionário das Tribos", "bio": "Autor best-seller e guru do marketing moderno. Criador dos conceitos Purple Cow e Tribes, pioneiro em permission marketing...", "expertise": ["Permission Marketing", "Purple Cow", "Tribes", "Storytelling Digital", "Nicho e Posicionamento"], "avatar": "/avatars/seth-godin.jpg", "category": "content"},
        {"key": "ann_handley", "id": "e8f6a3d1-b1c3-4d1c-8b2a-1c9e8f6a3d1b", "name": "Ann Handley", "title": "A Rainha do Content Marketing", "bio": "Chief Content Officer da MarketingProfs, autora de 'Everybody Writes'. Pioneira em content marketing...", "expertise": ["Content Marketing", "Everybody Writes", "Brand Voice", "Editorial Strategy", "Human Writing"], "avatar": "/avatars/ann-handley.jpg", "category": "content"},
        {"key": "neil_patel", "id": "b2a1c9e8-f6a3-4d1c-8b2a-1c9e8f6a3d1b", "name": "Neil Patel", "title": "A Lenda do Growth Hacking", "bio": "Co-fundador da NP Digital e Ubersuggest, reconhecido como top influencer em digital marketing...", "expertise": ["SEO", "Ubersuggest", "Content Decay", "Technical SEO", "Data-Driven Marketing"], "avatar": "/avatars/neil-patel.jpg", "category": "seo"},
        {"key": "gary_vaynerchuk", "id": "c9e8f6a3-d1b2-4d1c-8b2a-1c9e8f6a3d1b", "name": "Gary Vaynerchuk", "title": "O Rei das Mídias Sociais", "bio": "Empreendedor serial, investidor e especialista em redes sociais. Conhecido por sua abordagem direta, foco em personal branding...", "expertise": ["Social Media", "Personal Branding", "Day Trading Attention", "Content Creation", "Entrepreneurship"], "avatar": "/avatars/gary-vaynerchuk.jpg", "category": "social"},
        {"key": "sean_ellis", "id": "a3d1b2a1-c9e8-4d1c-8b2a-1c9e8f6a3d1b", "name": "Sean Ellis", "title": "O Criador do Growth Hacking", "bio": "Criador do termo 'growth hacking', autor de 'Hacking Growth'. Desenvolveu o ICE Framework...", "expertise": ["Growth Hacking", "ICE Framework", "40% Rule PMF", "Dropbox Referral", "Activation Optimization"], "avatar": "/avatars/sean-ellis.jpg", "category": "growth"},
        {"key": "brian_balfour", "id": "d1b2a1c9-e8f6-4d1c-8b2a-1c9e8f6a3d1b", "name": "Brian Balfour", "title": "O Estrategista de Growth", "bio": "Founder & CEO da Reforge, ex-VP Growth @ HubSpot. Criador do Four Fits Framework e defensor de Growth Loops...", "expertise": ["Four Fits Framework", "Growth Loops", "Market-Product Fit", "Reforge", "Strategic Alignment"], "avatar": "/avatars/brian-balfour.jpg", "category": "growth"},
        {"key": "andrew_chen", "id": "e8f6a3d1-b2a1-4d1c-8b2a-1c9e8f6a3d1b", "name": "Andrew Chen", "title": "O Mestre dos Network Effects", "bio": "General Partner @ Andreessen Horowitz, ex-Head of Rider Growth @ Uber. Autor de 'The Cold Start Problem'...", "expertise": ["Network Effects", "Cold Start Problem", "Marketplace Dynamics", "Atomic Networks", "Uber Growth"], "avatar": "/avatars/andrew-chen.jpg", "category": "growth"},
        {"key": "jonah_berger", "id": "f6a3d1b2-a1c9-4d1c-8b2a-1c9e8f6a3d1b", "name": "Jonah Berger", "title": "O Cientista da Viralidade", "bio": "Professor @ Wharton, autor de 'Contagious: Why Things Catch On'. Criador do STEPPS Framework...", "expertise": ["STEPPS Framework", "Viral Marketing", "Word-of-Mouth", "Contagious Content", "Social Currency"], "avatar": "/avatars/jonah-berger.jpg", "category": "viral"},
        {"key": "nir_eyal", "id": "8a3e792a-3b9c-4f0d-8a6e-3c9c7d1c9f0a", "name": "Nir Eyal", "title": "Mestre em Psicologia do Produto", "bio": "Autor de 'Hooked' e 'Indistractable', especialista em design comportamental e na criação de produtos que formam hábitos.", "expertise": ["Design Comportamental", "Modelo Hooked", "Psicologia do Consumidor", "Engajamento de Produto", "Retenção de Usuários"], "avatar": "/avatars/nir-eyal.jpg", "category": "product"},
    ]

    legends_data = []
    for meta in base_legends:
        prompt = LEGENDS_PROMPTS.get(meta["key"])  # type: ignore[attr-defined]
        if not prompt:
            print(f"⚠️ Skipping legend '{meta['name']}' because prompt '{meta['key']}' is not available.")
            continue
        legends_data.append({
            "id": meta["id"],
            "name": meta["name"],
            "title": meta["title"],
            "bio": meta["bio"],
            "expertise": meta["expertise"],
            "systemPrompt": prompt,
            "avatar": meta.get("avatar"),
            "category": meta["category"],
        })

    experts_created = 0
    for legend in legends_data:
        # Check if expert already exists in the database/storage
        existing_expert = await storage.get_expert(legend["id"])
        
        if existing_expert:
            # print(f"Expert {legend['name']} already exists. Skipping.")
            continue

        expert_data = ExpertCreate(
            name=legend["name"],
            title=legend["title"],
            expertise=legend["expertise"],
            bio=legend["bio"],
            systemPrompt=legend["systemPrompt"],
            avatar=legend.get("avatar"),
            expertType=ExpertType.HIGH_FIDELITY,
            category=CategoryType(legend["category"])
        )
        
        await storage.create_expert(expert_data, expert_id=legend["id"])
        experts_created += 1
        print(f"  -> Created expert: {legend['name']}")

    if experts_created > 0:
        print(f"✅ Successfully created {experts_created} new marketing legends.")
    else:
        print("✅ All marketing legends already exist in the database.")

    # Set the in-memory flag after seeding to prevent re-runs in dev mode
    if isinstance(storage, MemStorage):
        storage._legends_seeded = True
