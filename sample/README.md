# Team NOVA

## Team members:
Wissal Khlouf, Aileen Kent, and Ruth Melese


## Data Source:

For this project, we used the GitHub REST API to study the commit history of five major Python libraries, which are pandas, NumPy, scikit-learn, matplotlib, and PyTorch. The API gave us access to detailed commit metadata, including authors, timestamps, messages, and links back to each change. This API allowed us to pull several years of development activity across all five libraries.

## Challenges / Obstacles:

There's a limit for authenticated and unauthenticated pulls, so we had to work around that. GitHub returns data in pages of 100 items at a time, so it took a while for the data to loop through page after page to gather everything. To manage this, we built a pipeline that uses batching and a DuckDB database so the data would load cleanly and be analyzed quickly after collection.

## Analysis:

Offer a brief analysis of the data with your findings. Keep it to one brief, clear, and meaningful paragraph.


## Plot / Visualization:

Include at least one compelling plot or visualization of your work. Add images in your subdirectory and then display them using markdown in your README.md file.

## GitHub Repository:

[https://github.com/](https://github.com/aileenkent/dp3-github-dashboard)
