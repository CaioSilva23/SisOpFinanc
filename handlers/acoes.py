from handlers.auth import auth
from .base import Base
from database.models import Conexao


@auth
class AcoesHandler(Base):
    """list acoes disponíveis"""
    def get(self):
        acoes = self.acoes_list()
        if acoes:
            return self.write({"Ações":
                    [{"id": acao.id,
                      "name": acao.name,
                      "description": acao.description,
                      "price_unit": acao.price_unit,
                      "stock": acao.stock}
                        for acao in acoes]})
        return self.write({"info": "nenhuma ação disponível a venda!"})

    def post(self):
        """post ação"""
        data = self.data()

        name = data.get('name')
        description = data.get('description')
        price_unit = data.get('price_unit')
        stock = data.get('stock')

        try:
            self.save_acao(
                name=name,
                description=description,
                price_unit=price_unit,
                stock=stock
            )
            self.write({"message": "Acao created successfully"})
        except Exception as e:
            self.write({"error": f"error ao salvar a ação {e}"})


@auth
class AcaoHandler(Base):
    """ações detail"""
    def get(self, id):
        acao = self.acao_get_id(id=id)
        if not acao:
            self.set_status(404)
            return self.write({'error': {'acao': 'Ação not found'}})
        return self.write({"Ação":
                           {"id": acao.id,
                            "name": acao.name,
                            "description": acao.description,
                            "price_unit": acao.price_unit,
                            "stock": acao.stock
                            }})


@auth
class AcoesForUserHandler(Base):
    def get(self):
        minhas_acoes = self.list_acoes_for_user()

        if not minhas_acoes:
            return self.write({"Ações": "Voce não possui ações!"})
        return self.write(
            {"Suas ações":
                [{"operation": operacoes.id,
                    "date": f'{operacoes.date}',
                    "name": operacoes.acao.name,
                    "description": operacoes.acao.description,
                    "quantity": operacoes.quantity,
                    "value": operacoes.price_total
                  }
                    for operacoes in minhas_acoes]}
                    )

    def post(self):
        id = self.data().get('operacao')
        valor_unit = self.data().get('valor_unit')
        quantidade = self.data().get('quantity')
        operacao = self.operation_get_id(id=id)
        session = Conexao.cria_session()

        if operacao.quantity < quantidade:
            return self.write({"error": f"quantidade insuficiente, voce possui {operacao.quantity}"})  # noqa

        try:
            operacao.quantity -= quantidade
            operacao.price_total = operacao.quantity * operacao.price_unit

            self.save_acao(
                name=operacao.acao.name,
                description=operacao.acao.description,
                price_unit=valor_unit,
                stock=quantidade
            )

            self.save_operation(
                acao_id=operacao.acao.name,
                type_operation='Venda',
                quantity=quantidade,
                price_venda=valor_unit,
               )

            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
            return self.write({"success": "ação vendida com sucesso!"})
