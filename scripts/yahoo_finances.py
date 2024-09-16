import os
import yfinance as yf
import pandas as pd
from commons.configs import LoadConfigs
import logging as log


class YahooFinances():
    def __init__(self):
        # Configuração dos diretórios e do logger
        self.configs = LoadConfigs()
        # Leitura do arquivo de entrada
        input_file = os.path.join(
            self.configs.get_input_datas_dir(), "input_buy_stock.csv")
        self.INPUT_BUY_STOCKS = open(
            input_file, 'r', encoding='utf-8').readlines()

        # Lista para armazenar os dados do rendimento
        self.rendimento_dados = []

    def calcular_rendimento(self, TICKER, DATA_COMPRA, QTD_COTAS):
        try:
            # Obter os dados históricos da ação
            acao = yf.Ticker(TICKER)

            # Definir um intervalo de tempo
            start_date = pd.to_datetime(DATA_COMPRA)
            end_date = pd.Timestamp.today()

            # Obter o histórico de preços
            historico = acao.history(start=start_date, end=end_date)

            if historico.empty:
                log.warning(
                    f"Nenhum dado histórico encontrado para {TICKER} entre {start_date.date()} e {end_date.date()}.")
                return

            # Converter datas para formato sem timezone
            historico.index = historico.index.tz_localize(None)  # type: ignore

            # Encontrar a data mais próxima da data de compra
            historico['Date'] = historico.index
            historico['Diff'] = abs(
                historico['Date'] - pd.to_datetime(DATA_COMPRA))
            data_mais_proxima = historico.loc[historico['Diff'].idxmin(
            )]['Date']

            # Selecionar o preço de fechamento na data mais próxima
            preco_compra = historico.loc[historico['Date']
                                         == data_mais_proxima, 'Close'].values[0]
            valor_total_compra = preco_compra * QTD_COTAS

            log.info(
                f"Você comprou {QTD_COTAS} cotas de {TICKER} em {data_mais_proxima.date()} a {preco_compra:.2f} cada.")
            log.info(f"Valor total investido: R${valor_total_compra:.2f}")

            # Obter os dividendos
            dividendos = acao.dividends

            if dividendos.empty:
                log.warning(f"Nenhum dividendo encontrado para {TICKER}.")
                return

            # Converter o índice para datetime
            dividendos.index = pd.to_datetime(dividendos.index)

            # Agrupar dividendos por ano
            dividendos_anuais = dividendos.groupby(
                dividendos.index.year).sum()  # type: ignore

            # Calcular os rendimentos totais com base na quantidade de cotas
            dividendos_totais = dividendos_anuais * QTD_COTAS

            # Total de dividendos
            total_dividendos = dividendos_totais.sum()

            # Salvar os dados do rendimento em uma lista
            self.rendimento_dados.append({
                'TICKER': TICKER,
                'DATA_COMPRA': data_mais_proxima.date(),
                'PRECO_COMPRA': preco_compra,
                'QTD_COTAS': QTD_COTAS,
                'VALOR_TOTAL_COMPRA': valor_total_compra,
                'DIVIDENDOS_TOTAIS': total_dividendos,
                'RETORNO_TOTAL': total_dividendos + valor_total_compra
            })

            log.info(
                f"Retorno total com dividendos: R${total_dividendos + valor_total_compra:.2f}")

        except Exception as e:
            log.exception(f"Ocorreu um erro ao calcular o rendimento: {e}")

    def salvar_rendimentos_csv(self, output_file):
        # Converter a lista de dados em um DataFrame
        df_rendimento = pd.DataFrame(self.rendimento_dados)

        # Verificar se o arquivo já existe
        if not os.path.isfile(output_file):
            # Se o arquivo não existe, criar um novo com cabeçalhos
            df_rendimento.to_csv(output_file, index=False,
                                 mode='w', encoding='utf-8')
        else:
            # Se o arquivo já existe, adicionar os dados sem reescrever o cabeçalho
            df_rendimento.to_csv(output_file, index=False,
                                 mode='a', header=False, encoding='utf-8')

        log.info(f"Dados de rendimento salvos em {output_file}")
