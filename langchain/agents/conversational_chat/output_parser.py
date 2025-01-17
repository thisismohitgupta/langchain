from __future__ import annotations

import json
from typing import Union

from langchain.agents import AgentOutputParser
from langchain.agents.conversational_chat.prompt import FORMAT_INSTRUCTIONS
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re

class ConvoOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        cleaned_output = text.strip()

        print(cleaned_output)

        action_pattern = r'"action":\s*"([^"]*)"'
        action_input_pattern = r'"action_input":\s*"([^"]*)"'

        action_match = re.search(action_pattern, cleaned_output)
        action_input_match = re.search(action_input_pattern, cleaned_output)


        try:
            if action_match is None or action_input_match is None:
                raise ValueError(
                    "Failed to parse values from the LLM output: ", cleaned_output
                )

                action = action_match.group(1)
                action_input = action_input_match.group(1)
                print(action_input, action)

                parsed = {"action": action, "action_input": str(action_input)}
                parsed_output = json.dumps(parsed)
            else:
                if "action_input" in cleaned_output or "action_input" in json.loads(cleaned_output):
                    return AgentFinish({"output": json.loads(cleaned_output)['action_input']}, text)

        except Exception as e:
            print("Failed to parse LLM output: ", cleaned_output)

        try:
            response = json.loads(parsed_output)
            action, action_input = response["action"], response["action_input"]

        except Exception as e:
            print(action_match)
            if action_match != None:
                action, action_input = action_match.group(1), cleaned_output
            else:
                action = "Final Answer"
                action_input = cleaned_output

        if action == "Final Answer":
            print("doggy")
            return AgentFinish({"output": action_input}, text)
        else:
            print("doggy2")
            return AgentAction(action, action_input, text)

