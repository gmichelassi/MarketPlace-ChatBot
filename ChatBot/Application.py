from .Retriever import Retriever

from configs import CONTEXT_DATABASE_SOURCE, contextualization_system_prompt, system_prompt

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


class ChatBot:
    def __init__(self):
        self.context_database_source = CONTEXT_DATABASE_SOURCE
        self.contextualization_system_prompt = contextualization_system_prompt
        self.system_prompt = system_prompt

        self.model = ChatOpenAI(model="gpt-4o", temperature=0.15)
        self.retriever = self.__get_retriever()

        self.store = {}

    def ask(self, session_id: str, message: str):
        conversation = self.__conversational_rag_chain()

        return conversation.invoke(
            {"input": message},
            config={
                "configurable": {"session_id": session_id}
            },
        )["answer"]

    def __conversational_rag_chain(self):
        return RunnableWithMessageHistory(
            self.__rag_chain(),
            self.__get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def __get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()

        return self.store[session_id]

    def __rag_chain(self):
        question_answer_chain = create_stuff_documents_chain(self.model, self.__prompt())

        history_aware_retriever = create_history_aware_retriever(
            self.model, self.retriever, self.__contextualization_prompt()
        )

        return create_retrieval_chain(history_aware_retriever, question_answer_chain)

    def __contextualization_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.contextualization_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def __prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

    def __get_retriever(self):
        return Retriever(source=self.context_database_source).get_context()
