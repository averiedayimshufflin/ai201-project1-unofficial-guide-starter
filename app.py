import gradio as gr

from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""

    result = ask(question)

    source_lines = []

    for source in result["sources"]:
        source_lines.append(
            f"- {source['source']} | distance={source['distance']} | {source['url']}"
        )

    return result["answer"], "\n".join(source_lines)


with gr.Blocks() as demo:
    gr.Markdown("# UMD CS Professor Review Guide")
    gr.Markdown(
        "Ask a question about UMD CS professor reviews. "
        "The answer is generated only from retrieved project documents."
    )

    question = gr.Textbox(label="Your question")
    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=6)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources])
    question.submit(handle_query, inputs=question, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()