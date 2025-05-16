# Writing Team Documentation

This documentation outlines the structure and functionality of the `Writing Team`, an AI-powered team designed to collaboratively create blog post articles.

The Researcher Agent is designed to find information online related to the specified topic. It acts like an experienced online researcher specializing in making money online, including areas like affiliate marketing, paid advertising, content marketing, and SEO. Its primary goal is to use the information it finds on the internet to create a structured outline for an article on this topic. The Researcher uses the `GoogleSearchTools` to perform its research and is expected to output this article outline, which will then be passed on to the Writer Agent.

## Run the team with a task

1. Define the topic in the code.

```python
# ------------------------- Define the Topic --------------------------------
topic = "Your topic for the blog post"
# ---------------------------------------------------------------------------
```

2. Run the agent

```python
python content_writer.py
```
