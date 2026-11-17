# Episode 1 script, English (spoken; same structure as the Chinese v2)

【0 Hook】
How can Claude Code read files and get work done on its own? Because behind it, there is a loop. Today I'll write that loop in about fifty lines of Python. This is episode one of a new series: building a Claude Code style agent from scratch. Episode one covers just one thing: the core of an agent is a loop.

【1 What you need】
First, what you need. A computer that runs Python, a terminal, and an API key for a large language model. Our code follows Anthropic's message format, so both Claude's API and DeepSeek's API work. You only change one environment variable. In this series I'll demo with DeepSeek's model, because it's cheap. One note: a Claude Pro subscription does not include API access. To use Claude, create a key in the developer console, and pay for it separately.

【2 What is an agent】
What is an agent? Anthropic's engineering article describes agents as typically just language models using tools, based on feedback from the environment, in a loop. Three keywords: model, tools, loop. A chatbot answers when you ask, and that's the end. An agent is different. It decides for itself whether to look something up first, reads the result, and then decides the next step. Think of a new intern: you give them a task, they check the material, do one step, look at the result, and keep going until it's done.

【3 Claude Code's loop】
The official Claude Code documentation splits its work into three phases: gather context, take action, and verify results. These phases blend together, and repeat. Say you fix a bug. Reading files is gathering context. Editing code is taking action. Running tests is verifying results. So when does it stop? The Agent S D K documentation is clear: when the model's reply contains no tool calls, the loop ends. It also says the S D K runs the same loop that powers Claude Code. So what we build today is the smallest version of the same idea.

【4 One round】
Let's look at what happens in one round. Step one: we send the user's question to the model. Step two: the model doesn't answer directly. It replies with a block called tool use, which means: please call this tool, with these arguments. Notice that in our program, the model executes nothing. It only makes a request. Step three: our code actually runs the tool and gets the result. Step four: we wrap the result in a tool result block and send it back. The model reads it, and decides: use another tool, or answer. That's one round. Why does the result go in a user message? Because in this A P I there are only two roles, user and assistant. The result comes from our side, so it counts as the user side.

The tool use block has three fields. I D is the number of this request. Name is the tool's name. Input is the arguments. The tool result we send back must carry the same I D, so the model knows which request it answers. Sometimes the model makes several requests in one reply. Then we run all of them, and send all the results back together, in one message.

One more thing that is easy to miss: the model has no memory of its own. On every call, we send the complete messages list again. So the longer the conversation gets, the more we send each round, and the more it costs. We'll fix that in a later episode.

【5 The code】
Now the code. There are really only four things. One: make a messages list, starting with the user's question. Two: call the model, and append its reply to messages as it is. Three: look at the stop reason. If it isn't tool use, the loop ends, and we return the answer. Four: if it is, run each tool it asked for, wrap each result as a tool result, put them in one user message, append that to messages, and go back to step two. That's the whole loop. The stop reason has three common values. End turn means the model is finished. Tool use means it wants a tool. Max tokens means the answer was too long and got cut off. Our code only checks whether it's tool use. There's also a short system prompt that tells the model its role. We keep it very simple for now.

We only need one tool, called list files, which lists the files in a folder. A tool has three parts: a name, a description, and the format of its arguments. The model reads the description to decide when to use it, so write it clearly. When a tool fails, don't crash the program. Return the error as the result, and the model can usually find another way. Finally, add a safety limit: at most ten turns.

【6 Run it】
Let's run it. Ask: what is in this folder? On the first turn, the stop reason is tool use, and the model asks for list files. We run it and return the file names. On the second turn, the model has the file names, and usually just answers, and the stop reason becomes end turn, so the loop ends. The code prints the stop reason and the tool call on every turn. Watching each step is the most useful habit for understanding an agent. Now let's ask about a folder that doesn't exist. The tool returns an error. An error is just another kind of result. The model reads it, then tells you, or tries another path. After the two-turn example, the messages list holds four messages. First, user: our question. Second, assistant: a tool use. Third, user: the tool result, which is the file names. Fourth, assistant: the final answer. Those four are the full record of the task.

【7 When to stop】
When does it stop? Two common cases. One is a normal ending: the model's reply has no tool calls. The other is that we stop it by force: the turn limit is reached. The Agent S D K has this option too, called max turns. The default is no limit. If it's exceeded, you get an error max turns result. Subagents in Claude Code can also have such a limit. So when you write your own, always add this safety. Otherwise the model keeps calling tools, the program never stops, and the money keeps burning.

【8 Three pitfalls】
Last, three easy mistakes. One: the tool result isn't sent back correctly. If the I D doesn't match, or one is missing, the A P I will usually return an error. Two: no turn limit, so the program runs on and keeps costing money. Three: thinking the model executed the code. Here, it is your program that does. So what is allowed, and what isn't, should also be decided by your program. That is exactly what the permissions episode is about.

【9 What's missing】
Looking back, what we built is still far from Claude Code. It has tools to read files, edit files and run commands. It has permissions, so dangerous actions ask you first. When the context gets full, it compacts automatically. It can hand tasks to subagents. We'll add these one by one later. This episode covered four things: the messages list, tools, the stop reason, and the turn limit. Remember one sentence: the core of an agent is a loop. Call the model, run the tools, give the results back, until it stops asking for tools. Next episode, we give it truly useful tools. Which part do you want to see first? Tell me in the comments.
