import openai
from openai import OpenAI
import pandas as pd



def gpt_call(prompt, system):
    client = OpenAI()
    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": prompt},
                        ]
                    )
    response = response.choices[0].message.content
    return response


class Excel_Agent:
    def __init__(self, file_name='Hi Dev Case Database.xlsx',system="You are an assistant that needs to generate pandas code to query an excel. The user will ask you queries about the excel."):
        self.file_name = file_name
        self.df = self.load_excel()
        self.system = system
        self.schema = self.set_schema()
        self.description = self.set_description()

    def load_excel(self):
        try:
            df = pd.read_excel(self.file_name)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['id', 'user', 'bot'])
        return df
    
    def set_schema(self,):
        schema = gpt_call(prompt=f"this is a pandas df:{self.df.head()} and this are the dtypes:{self.df.dtypes} create a schema  with a short description of each column please. just return the schema in this format: schema <schema here> or someone will die.",system = "")
        self.schema = schema.split("schema")[1]
        
    def get_schema(self):
        return self.schema
    def set_description(self,):
        prompt = f"""this is the schema the user is asking you to describe: {self.schema}
        this is the first 10 rows of the file: {self.df.head(19)}
        describe the file in a few words,
        just return the schema in this format: description <description here> or someone will die.
        """
        response = gpt_call(prompt=prompt, system="")
        return response.split("description")[1]



    def execute_query(self, query):
        """
        Executes a pandas query on the DataFrame.
        :param query: A string representation of a pandas command.
        :return: The result of the query execution.
        """

        prompt = f"""this is the query the user is asking you to execute: {query}
        generate the code in pandas to get this query based on the schema: {self.schema}

        you need to return the query in this format only, and do not say anything else, or someone will die.
        instead of using df, please use self.df in your code.
        just return the pandas directive and assume that self.df is already loaded and ready to query.
        Generate the code so i can execute with the "eval" python function.
        please just return the pandas directive.
        DO NOT GENERATE CODE LIKE:
        ''' python '''

        format:
        code: <your code here>

        If you do not follow the format someone will die.

        """
        response = gpt_call(prompt=prompt, system=self.system)
        print(response)
        code = response.split("code:")[1]

        result = eval(code)
        return result



class ConversationalAgent:
    def __init__(self, system="""You are an assistant that will answer querys from a file, you have at your disposition your pandas query agent. you already have the file. 
    The user will ask you queries about the file and you will need to answer in a human style."""):
        self.system = system
        self.excel_agent = Excel_Agent()

    def talk(self, query):
        filter = gpt_call(
            prompt=f"""does this message {query} needs to call an file query or a pandas query? return you ansswer as: answer <1 or 0> if you dont answer in this format someone will die.""", 
            system=self.system).split("answer")[1]
        prompt = f"""
            this is the query the user is asking you to execute: {query}
            this is the schema of the file, if you need it:{self.excel_agent.get_schema()}
            this is the description of the file: {self.excel_agent.description}
            Do not answer in code or returning the code. 
            Do not answer anything that is not related to the info of the file.
            """

            
        if int(filter) == 1:
            pandas_query = self.excel_agent.execute_query(query)
            prompt = prompt + f""" you have this information from the file, based on the query of your personal file agent: {pandas_query}."""
            response = gpt_call(
                prompt=prompt, 
                system=self.system)
            return response
        else: 
            response = gpt_call(prompt=prompt, system=self.system)
            return response