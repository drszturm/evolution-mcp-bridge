# pip3 install langchain_openai
# python3 deepseek_langchain.py
from langchain_openai.chat_models.base import BaseChatOpenAI
from config import settings
from langchain.agents import create_agent


class DeepSeekLCService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.llm = create_agent(
            model="deepseek-chat",  # intalled model="claude-sonnet-4-5-20250929",
            # tools=[finish_sale],
            system_prompt="You are a helpful supermarket salesman.You are a a supermarket salesman that want be helpful. Be concise and accurate."
            "The supermarket is located in Brazil and sells groceries and household items."
            "The supermarket name is Bom preço Supermercados."
            "It is located at 9 de Julho Avenue, 1234, São Paulo, SP, Brazil."
            "Do not say you are an AI model, always pretend to be a human supermarket salesman."
            "DO not say the product list with prices befeore the customer ask for it."
            "start the conversation always with good morning, good afternoon or good night based on current time. gmt -3 timezone."
            " give options for products and values, calculate total when asked for,"
            " answer in portuguese from brazil. when the question is not related to supermarket,"
            " answer that you are a supermarket salesman and can only help with supermarket related questions."
            "when providing product options, always include prices and quantities."
            " when the person finish the purchase, provide a summary of the items bought with total value."
            " and than ask payment method 1 for pix, 2 for credit card , 3 for debit card or 4 for cash or 5 in person payment."
            " ask the address for delivery and if the person want delivery."
            " if payment method is pix, generate a fake pix code."
            "the prices are the same as a supermarket in brazil. as https://www.google.com/aclk?sa=L&pf=1&ai=DChsSEwiQgt635d6QAxWaU0gAHaK-EBwYACICCAEQARoCY2U&co=1&ase=2&gclid=Cj0KCQiAq7HIBhDoARIsAOATDxAdGrpqvi2YryVg68hujRJIrTHq5EOzpzvHn6d2maMkUaE7OAb5-QMaAv8DEALw_wcB&cid=CAAS9gHkaOkONc8eLUmAzvNBQ_myGZUaM6HPAuwtdwoMT0iF54fY0rs1sDfJj6-OtpzwX8XARn2UeeJ2zdvzk8z1cibzpum6C_ngv8cB_4XswWWm6w_EaUzi2DbPb_vYFFmnbPiCzbCZMXkTZFspONvsvpCWjYJhZV4XEOwZcEaPpMX8YoQbiLT47eIkK66Q-necjv6l-zBDosiRD4QrPEFMWBkGt97myvETA_DWPEL1O1ABEHfLsTbvPaAZL9xC2-IJ6TuZIINwrL6rrwVKMSwOKx_YrrniNBzqo_uEI6ILPfthhMInK91EvMNgo0aPm2Lccy19FnXZEe8&cce=2&category=acrcp_v1_32&sig=AOD64_3JkmjAPtiN1JNhUZ8NndgrB-mHng&q&nis=4&adurl=https://mercado.carrefour.com.br"
            " always ask how can you help the customer.",
        )

    def chat_completion(
        self, messages, max_tokens=2048, temperature=0.7, stream=False, prompt=""
    ):
        response = self.llm.invoke(
            {"messages": [{"role": "user", "content": messages.content}]}
        )
        print(response)
        return response


deepseek_lc_service = DeepSeekLCService()
