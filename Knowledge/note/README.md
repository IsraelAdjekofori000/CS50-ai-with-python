
# Knowledge / II

In the real world, information is often incomplete or not directly known. A lot of useful information is embedded in complex relationships with other data points and scenarios. These details usually need to be mined by reasoning through intricate webs of interconnected data, much like solving a puzzle. Depending on who you ask, this can be a fun task. However, just like everything else, humans have limits when it comes to handling complex and tedious processes. This is where computers come in.

This directory implements a **proof of concept** algorithm (model checking) to address these challenges.

The implementation tackles two main pitfalls:

### 1. Knowledge Representation:
Real-world observations and their relationships in complex scenarios need a way to be represented on a computer for processing and manipulation.

For example, consider the scenario: "It’s Tuesday and it’s raining, so James can’t go to the market."

Though this is a simple example, from this statement, we can infer that it's Tuesday, it's raining, and James won’t go to the market because of these two conditions. The computer would need a way to store information about this scenario so that new inferences can be drawn. This is achieved through the use of **Assert** (for simple true statements), **And** & **Or** (for logical connections), and **Imply** & **BiConditional** (for logical relationships) — _see the notebook for examples of these in use_.

### 2. Knowledge Inference:
Since the goal is to derive new information from existing knowledge and relationships modeled for real-world scenarios, the system needs a way to infer these details. This is where the model checking algorithm comes in. _For more details, refer to the notebook_.

See the full video course on [Yotube](https://www.youtube.com/watch?v=HWQLez87vqM&list=PLhQjrBD2T381PopUTYtMSstgk-hsTGkVm&index=3&t=16s&pp=iAQB)
