from app import create_app, db
from app.models import Usuario, Produto
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # --- USUÁRIOS ---
    usuarios = [
        Usuario(
            nome='Admin',
            email='admin@sistema.com',
            senha=generate_password_hash('admin123'),
            perfil='ADMIN'
        ),
        Usuario(
            nome='João Silva',
            email='joao.silva@email.com',
            senha=generate_password_hash('cliente123'),
            perfil='CLIENTE',
            endereco='Rua Floriano Peixoto, 450',
            cidade='Campina Grande',
            estado='PB',
            cep='58400-001'
        ),
        Usuario(
            nome='Maria Oliveira',
            email='maria.o@email.com',
            senha=generate_password_hash('cliente123'),
            perfil='CLIENTE',
            endereco='Av. Manoel Tavares, 1200',
            cidade='Campina Grande',
            estado='PB',
            cep='58410-000'
        ),
        Usuario(
            nome='Ricardo Santos',
            email='ricardo.auto@email.com',
            senha=generate_password_hash('cliente123'),
            perfil='CLIENTE',
            endereco='Rua Getúlio Vargas, 88',
            cidade='João Pessoa',
            estado='PB',
            cep='58000-100'
        )
    ]

    for u in usuarios:
        if not Usuario.query.filter_by(email=u.email).first():
            db.session.add(u)


    dados_produtos = [
        # Filtros
        ('Filtro de Óleo Sedan', 'FT-001', 'Filtros', 35.50, 40),
        ('Filtro de Ar Esportivo', 'FT-002', 'Filtros', 89.90, 15),
        ('Filtro de Combustível Flex', 'FT-003', 'Filtros', 42.00, 25),
        ('Filtro de Cabine (Ar Cond.)', 'FT-004', 'Filtros', 55.00, 20),
        ('Filtro de Óleo Diesel', 'FT-005', 'Filtros', 75.00, 10),

        # Freios
        ('Pastilha de Freio Dianteira', 'FR-001', 'Freios', 120.00, 12),
        ('Disco de Freio Ventilado', 'FR-002', 'Freios', 245.00, 8),
        ('Cilindro Mestre de Freio', 'FR-003', 'Freios', 310.00, 5),
        ('Fluido de Freio DOT4 500ml', 'FR-004', 'Freios', 25.90, 50),
        ('Sapata de Freio Traseira', 'FR-005', 'Freios', 115.00, 10),
        ('Cabo de Freio de Mão', 'FR-006', 'Freios', 45.00, 15),

        # Suspensão e Direção
        ('Amortecedor Dianteiro', 'SS-001', 'Suspensão', 380.00, 6),
        ('Kit Batente Amortecedor', 'SS-002', 'Suspensão', 95.00, 20),
        ('Pivô de Suspensão', 'SS-003', 'Suspensão', 68.00, 14),
        ('Bucha da Bandeja', 'SS-004', 'Suspensão', 22.00, 30),
        ('Terminal de Direção', 'SS-005', 'Suspensão', 55.00, 12),
        ('Mola Helicoidal Traseira', 'SS-006', 'Suspensão', 190.00, 4),

        # Motor e Transmissão
        ('Correia Dentada HTD', 'MT-001', 'Motor', 85.00, 18),
        ('Tensor da Correia', 'MT-002', 'Motor', 130.00, 10),
        ('Bomba d\'Água HighFlow', 'MT-003', 'Motor', 210.00, 7),
        ('Jogo de Velas Iridium', 'MT-004', 'Motor', 160.00, 15),
        ('Cabo de Vela Magnético', 'MT-005', 'Motor', 110.00, 9),
        ('Junta do Cabeçote', 'MT-006', 'Motor', 145.00, 5),
        ('Radiador de Arrefecimento', 'MT-007', 'Motor', 450.00, 3),
        ('Aditivo para Radiador 1L', 'MT-008', 'Motor', 18.00, 100),
        ('Coxim do Motor Lado Direito', 'MT-009', 'Motor', 175.00, 6),
        ('Sensor de Oxigênio (Sonda)', 'MT-010', 'Motor', 280.00, 8),

        # Elétrica
        ('Bateria 60Ah Selada', 'EL-001', 'Elétrica', 420.00, 10),
        ('Alternador 90A Recond.', 'EL-002', 'Elétrica', 580.00, 2),
        ('Lâmpada H4 Super Branca', 'EL-003', 'Elétrica', 35.00, 40),
        ('Motor de Partida 12V', 'EL-004', 'Elétrica', 620.00, 3),
        ('Fusível Automotivo Kit 10un', 'EL-005', 'Elétrica', 12.00, 60),
        ('Relé Auxiliar 40A', 'EL-006', 'Elétrica', 15.00, 25),

        # Ferramentas
        ('Chave de Fenda Phillips', 'FM-001', 'Ferramentas', 15.00, 30),
        ('Chave de Boca 10mm', 'FM-002', 'Ferramentas', 12.00, 20),
        ('Torquímetro de Estalo', 'FM-003', 'Ferramentas', 350.00, 2),
        ('Alicate de Pressão', 'FM-004', 'Ferramentas', 45.00, 15),
        ('Jogo de Chaves Torx', 'FM-005', 'Ferramentas', 120.00, 8),
        ('Macaco Hidráulico Jacaré', 'FM-006', 'Ferramentas', 290.00, 4),
        ('Multímetro Digital', 'FM-007', 'Ferramentas', 85.00, 10),
        ('Carregador de Bateria Bivolt', 'FM-008', 'Ferramentas', 180.00, 5),

        # Acessórios e Diversos
        ('Limpador de Parabrisa 18"', 'AC-001', 'Acessórios', 28.00, 22),
        ('Tapete de Borracha Jogo', 'AC-002', 'Acessórios', 110.00, 10),
        ('Capa de Proteção P', 'AC-003', 'Acessórios', 140.00, 5),
        ('Aromatizante Carro Novo', 'AC-004', 'Acessórios', 9.90, 80),
        ('Suporte para Celular GPS', 'AC-005', 'Acessórios', 25.00, 35),
        ('Cera Automotiva Pasta', 'AC-006', 'Acessórios', 32.00, 18),
        ('Estopa para Polimento 200g', 'AC-007', 'Acessórios', 7.50, 45),
        ('Cabo de Chupeta 300A', 'AC-008', 'Acessórios', 65.00, 12),
        ('Triângulo de Sinalização', 'AC-009', 'Acessórios', 30.00, 15)
    ]

    for nome, codigo, categoria, preco, qtd in dados_produtos:
        if not Produto.query.filter_by(codigo=codigo).first():
            novo_p = Produto(
                nome=nome,
                codigo=codigo,
                categoria=categoria,
                preco=preco,
                quantidade=qtd,
                imagem = f"{codigo}.jpg"
            )
            db.session.add(novo_p)

    db.session.commit()
    print(f'Seed concluído! {len(dados_produtos)} produtos e 4 usuários verificados/adicionados.')