# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict, List

import gradio as gr

from xinference.client import RESTfulClient


class ChatInterface:
    def __init__(
        self,
        endpoint: str,
        model_uid: str,
    ):
        self.client = RESTfulClient(endpoint)
        self.endpoint = endpoint
        self.model_uid = model_uid

    def build_interface(self):
        model = self.client.get_model(self.model_uid)

        def flatten(matrix: List[List[str]]) -> List[str]:
            flat_list = []
            for row in matrix:
                flat_list += row
            return flat_list

        def to_chat(lst: List[str]) -> List[Dict[str, str]]:
            res = []
            for i in range(len(lst)):
                role = "assistant" if i % 2 == 1 else "user"
                res.append(
                    {
                        "role": role,
                        "content": lst[i],
                    }
                )
            return res

        def generate_wrapper(message: str, history: List[List[str]]) -> str:
            output = model.chat(
                prompt=message,
                chat_history=to_chat(flatten(history)),
                generate_config={"max_tokens": 512, "stream": False},
            )
            return output["choices"][0]["message"]["content"]

        return gr.ChatInterface(
            fn=generate_wrapper,
            examples=[
                "Show me a two sentence horror story with a plot twist",
                "Generate a Haiku poem using trignometry as the central theme",
                "Write three sentences of scholarly description regarding a supernatural beast",
                "Prove there does not exist a largest integer",
            ],
            title="Xinference Chat Bot",
        )
