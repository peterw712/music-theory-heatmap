from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def create_frequency_matrix(data, matrix_size):
    frequency_matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    for progression in data:
        for i in range(len(progression) - 1):
            frequency_matrix[progression[i] - 1, progression[i + 1] - 1] += 1
    return frequency_matrix


def plot_matrix(matrix):
    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap='viridis')

    # Set axis labels
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels(np.arange(1, matrix.shape[1] + 1))
    ax.set_yticklabels(np.arange(1, matrix.shape[0] + 1))

    # Rotate the tick labels and set their alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # Calculate the brightness of the color
            bg_color = im.norm(matrix[i, j])
            brightness = (bg_color * 2.0) - 1.0

            # Set the text color based on the brightness
            if brightness > 0.5:
                text_color = "black"
            else:
                text_color = "white"

            text = ax.text(j, i, matrix[i, j], ha="center", va="center", color=text_color)

    ax.set_title("Progression Frequency Matrix")
    fig.tight_layout()
   

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        matrix_size = int(request.form["matrix_size"])
        input_data = request.form["input_data"].splitlines()
        input_data = [[int(x.strip()) for x in line.split(',')] for line in input_data]

        frequency_matrix = create_frequency_matrix(input_data, matrix_size)

        img = io.BytesIO()
        plot_matrix(frequency_matrix)
        plt.savefig(img, format="png")
        img.seek(0)
        img_b64 = base64.b64encode(img.getvalue()).decode("utf-8")

        return render_template("result.html", matrix_size=matrix_size, frequency_matrix=frequency_matrix, img_b64=img_b64)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
