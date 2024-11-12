# Sistema de Locadora de Veículos

Este projeto é um sistema de locadora de veículos que permite o gerenciamento de locações, cadastro de veículos e clientes, além de uma interface gráfica para facilitar o uso.

## Equipe de Desenvolvimento

- Marcelo Henrique Nunes - Turma: ADS
- Matheus de Queiroz - Turma: SI
- Samuel Lopes Gomes - Turma: ADS
- Tiago Genari Caldeira - Turma: ADS

## Entidades Principais

1. **Pessoa**
   - Representa uma pessoa no sistema, podendo ser um cliente ou funcionário.
   - **Cliente**: Pessoa que realiza locações de veículos.
   - **Funcionário**: Pessoa que gerencia o sistema, realiza cadastros e locações.

2. **Carro**
   - Representa um veículo disponível para locação.
   - Atributos: modelo, marca, ano de fabricação, placa, status de disponibilidade.

3. **Locação**
   - Representa o aluguel de um carro, incluindo data de início, data de término, carro alugado, cliente e funcionário responsável.

4. **Reserva**
   - Representa uma reserva automática feita para um carro assim que uma locação é realizada, com informações sobre o carro e o cliente.

## Funcionalidades do Sistema

1. **Cadastro de Carro**: Cadastro de novos veículos para locação.
2. **Consulta de Carro**: Consulta detalhada dos veículos cadastrados.
3. **Atualização de Status do Carro**: Atualiza o status dos veículos.
4. **Edição de Carro**: Permite editar informações como modelo, ano e valor de locação.
5. **Cadastro de Cliente**: Cadastro de novos clientes.
6. **Cadastro de Funcionário**: Cadastro de funcionários responsáveis pela gestão.
7. **Locação de Veículo**: Permite que clientes aluguem veículos.
8. **Devolução de Veículo**: Registra a devolução e atualiza o status do carro e da locação.

## Aspectos Técnicos Importantes

- **Relacionamentos entre Entidades**: Utilizamos o SQLAlchemy para modelar os relacionamentos entre clientes, locações, carros e reservas.
- **Operações CRUD**: As operações de criação, leitura, atualização e exclusão foram implementadas para todas as entidades principais.
- **Tratamento de Exceções**: Exceções tratadas para evitar erros, como tentativa de locação de um carro já alugado ou CPF duplicado em cadastros.
- **Interface de Usuário (UI)**: Desenvolvida com a biblioteca Tkinter, proporcionando uma interface gráfica simples e intuitiva para facilitar a interação.

## Bibliotecas Utilizadas

- **Tkinter**: Biblioteca utilizada para criação da interface gráfica, permitindo que os usuários realizem operações como cadastro, locação e consulta de maneira intuitiva.

---
