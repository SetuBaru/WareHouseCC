from openai import OpenAI
from pydantic import BaseModel
import instructor
from instructor.exceptions import InstructorRetryException
from tenacity import Retrying, retry_if_not_exception_type, stop_after_attempt


def ExtractEntity(_input_):
    # Making the inputs lowercase for easier processing
    _input_ = _input_.lower()

    class EntityDetail(BaseModel):
        processType: str
        transactionType: str
        itemName: str
        locationFrom: str
        locationTo: str

    retries = Retrying(
        retry=retry_if_not_exception_type(ZeroDivisionError), stop=stop_after_attempt(3)
    )

    # enables `response_model` in create call
    client = instructor.from_openai(
        OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # required, but unused
        ),
        mode=instructor.Mode.JSON,
    )

    models = ['nuextract', 'llama3:instruct']

    try:
        response = client.chat.completions.create(
            model=models[1],
            messages=[
                {"role": "system",
                 "content": '''You are a warehouse operating system that analyzing user queries and extracts entities. 
                 You should be very accurate and efficient, do not make up values & deal with the user input as it is! 
                 Your task is to identify and extract the following entities: processType: Can only be one of three 
                 values: "transaction": for messages related to a warehouse operation (either move, adjust or dispose). 
                 "greeting": for non-transactional greeting messages (greetings). "out_of_scope": for everything non 
                 "transactional" & non "greeting", anything in general (processType becomes out_of_scope) 
                 transactionType: Can be one of four types based on the operation described: "N/A" if processType is a 
                 greeting or out_of_scope, "move" for transferring an item from one location to another, "adjust" for 
                 updating quantities in the system, "dispose" for discarding/disposing of an item. ` itemName: The name 
                 or ID of the item involved in the transaction (if not applicable then N/A). "locationFrom": The starting 
                 location for the item involved in the transaction (if not applicable then N/A). " locationTo": The 
                 destination location for the item involved in the transaction (if not applicable then N/A). Make Sure to 
                 provide any response to the user in the form of "processType='value' transactionType='value' 
                 itemName='value' locationFrom='value' locationTo='value'".'''
                 },
                {"role": "user", "content": _input_},
            ],
            response_model=EntityDetail,
            max_retries=retries,
        )

        # Convert response to dictionary if it's an EntityDetail object
        if isinstance(response, EntityDetail):
            return response.dict()  # Convert to dictionary

        return response

    except InstructorRetryException as e:
        print(e.messages[-1]["content"])  # type: ignore
        """
        1 validation error for UserDetail
        age
        Value error, You will never succeed with 25 [type=value_error, input_value=25, input_type=int]
            For further information visit https://errors.pydantic.dev/2.7/v/value_error
        """

        print(e.n_attempts)
        # > 3

        print(e.last_completion)
        """
        ChatCompletion(id='chatcmpl-9FaHq4dL4SszLAbErGlpD3a0TYxi0', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_XidgLpIu1yfaq876L65k91RM', function=Function(arguments='{"name":"Jason","age":25}', name='UserDetail'), type='function')]))], created=1713501434, model='gpt-3.5-turbo-0125', object='chat.completion', system_fingerprint='fp_d9767fc5b9', usage=CompletionUsage(completion_tokens=27, prompt_tokens=513, total_tokens=540))
        """


if __name__ == "__main__":
    ExtractEntity("move x from 1 to 2")
