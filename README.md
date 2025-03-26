# Simulated Annealing para SAT

Este projeto implementa o algoritmo **Simulated Annealing** para resolver problemas de **Satisfação Booleana (SAT)**, verificando se uma sequência de valores **True** e **False** satisfaz uma determinada fórmula lógica.

## 🧠 Como funciona?
O **Simulated Annealing (SA)** é um algoritmo de otimização inspirado no processo físico de recozimento. Ele busca uma solução ótima explorando gradualmente o espaço de busca e evitando mínimos locais ao aceitar soluções piores com certa probabilidade.

### 🔥 Etapas do algoritmo:
1. **Inicialização:** Começa com uma atribuição aleatória de valores para as variáveis do SAT.
2. **Geração de Vizinhança:** Modifica uma única variável (ou um pequeno número delas) por vez.
3. **Avaliação da Solução:** Verifica quantas cláusulas da fórmula são satisfeitas.
4. **Critério de Aceitação:**
   - Se a nova solução for melhor, aceita automaticamente.
   - Se for pior, aceita com uma **probabilidade sigmoide**:
     
     \[ P(\text{aceitar}) = \frac{1}{1 + \exp(\frac{\Delta E}{T})} \]
     
     Onde:
     - \( \Delta E \) é a variação da função de custo (quantidade de cláusulas insatisfeitas).
     - \( T \) é a temperatura atual do sistema.
5. **Resfriamento:** A temperatura diminui a cada iteração para refinar a busca.
6. **Critério de Parada:** O processo continua até atingir uma temperatura mínima ou um número máximo de iterações.

## 📌 Recursos
- Implementação eficiente do **Simulated Annealing**.
- Função de aceitação baseada em **sigmoide** para suavizar a decisão.
- Configuração ajustável de parâmetros como temperatura inicial, taxa de resfriamento e número de variáveis modificadas por iteração.
- Aplicação ao problema de **SAT** para encontrar uma atribuição de variáveis que satisfaça a fórmula lógica.

## 🚀 Como rodar o código?
1. Instale dependências, se necessário:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o script:
   ```bash
   python simulated_annealing_sat.py
   ```

## 📚 Referências


---
📌 **Autor:** Guilherme Diel  

