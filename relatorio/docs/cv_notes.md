PRA PROXIMA QUARTA JA TER RESULTADOS INICIAIS

o proximo projeto vai ser usado o mesmo simulated annealing 
adaptando o código para o cenário do novo problema

problema: caixeiro viajante

aplicar o simulated annealing para o caixeiro viajante simétrico 2d
(encontrar o caminho minimo passando por todas as cidades sem repetir) (NP-Completo)

RESOLVER 2 INSTÂNCIAS

pode jogar fora os comentarios
pontos coordenados num plano cartesiano (usar distancia euclidiana)

solucao x = [2 1 3 5 4]
	custo = distancia(2,1) + distancia(1,3) + distancia(3,5) + distancia(5,4) + distancia(4,2)
fazer uma matriz (simétrica) de distancias – fazer um calculo de matriz diagonal pq é simétrica – fazer esse calculo antes de entrar no algoritmo

scritp:
- [ ] CARREGAR A INSTANCIA
- [ ] FAZER A MATRIZ NxN
- [ ] ESTRATEGIA PARA GERAR O VIZINHO
- [ ] FUNCAO OBJETIVO

também ajustar temperatura inicial, queda de temperatura, etc..

usar um vetor de inteiro perguntado(que nao pode repetir inteiro)

só quer o gráfico de convergencia e resultado da amostra, assim como no trabalho do SAT3, com SA_MAX 1, 5 e 10
￼
