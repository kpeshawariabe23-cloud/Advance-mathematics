# 🚀 Credit Card Fraud Detection: A Sampling Techniques Study

Hey there! Welcome to my repository for the **Sampling Assignment**. 

In this project, I tackled a classic machine learning problem: predicting credit card fraud. However, the main focus here wasn't just on throwing algorithms at the data. Instead, it was an in-depth exploration of how **different sampling techniques** impact the performance of various machine learning models, especially when dealing with a highly imbalanced dataset.

Let's dive into the details!

---

## 📊 1. The Dataset & The Imbalance Problem

I started with the `Creditcard_data.csv` dataset, which contains transaction records. The target variable is a binary class label indicating whether a transaction is fraudulent (`1`) or legitimate (`0`).

Right off the bat, I noticed a massive class imbalance:
- **Class 0 (Legitimate):** 763 transactions
- **Class 1 (Fraudulent):** 9 transactions

Training a model on this directly would be a disaster—it would likely just predict "0" every time and look highly accurate but be practically useless. So, the first challenge was to balance this out.

---

## 🛠️ 2. Step-by-Step Methodology

### Step 1: Balancing the Scales
Since the minority class had merely 9 instances, simply under-sampling the majority class would mean losing too much valuable data. So, I went with **Random Over Sampler**. 

By oversampling the minority class, I brought its count up to match the majority class (763). This gave me a perfectly balanced dataset of **1,526 rows** to work with.

### Step 2: Figuring Out the Sample Size
Next, I needed to determine the optimal sample size. I didn't just guess; I used **Cochran's Formula**. Assuming a 95% confidence level, a 5% margin of error, and an estimated proportion ($p$) of 0.5 (maximum variability), the math looked like this:

$$ n = \frac{Z^2 p(1-p)}{E^2} \approx 384 $$

So, I set my target sample size to **384** rows per sample.

### Step 3: Trying Different Sampling Flavors
To see how the models would react to different data distributions, I created 5 distinct samples using the following sampling techniques:

1. **Simple Random Sampling:** The classic approach—just randomly picking 384 rows from the balanced dataset.
2. **Systematic Sampling:** Calculated a step size ($k = N/n$) and selected every $k^{th}$ row.
3. **Stratified Sampling:** Ensuring that the proportion of each class in the sample matched the population (which, in this case, was already balanced 50/50).
4. **Cluster Sampling:** Grouped the data into artificial clusters and then randomly picked entire clusters until I reached the desired sample size.
5. **Bootstrap Sampling:** Sampled 384 rows with replacement, meaning some rows might appear multiple times.

### Step 4: The Machine Learning Lineup
With 5 differently sampled datasets ready to go, I trained and evaluated 5 different machine learning models on each one:

1. **Logistic Regression** (The baseline)
2. **Decision Tree** (The rule-maker)
3. **Random Forest** (The ensemble favorite)
4. **Support Vector Machine (SVM)** (The margin maximizer)
5. **Gradient Boosting** (The error corrector)

---

## 📈 3. The Results Matrix

After running all the models across all the samples, here's how they performed in terms of **Accuracy**. 

| Sampling Technique | Logistic Regression | Decision Tree | Random Forest | SVM | Gradient Boosting |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Simple Random** | 0.8621 | 0.9741 | 0.9828 | 0.9310 | 0.9741 |
| **Systematic** | 0.8889 | 0.9869 | **0.9935** | 0.9542 | **0.9935** |
| **Stratified** | 0.9052 | 0.9655 | 0.9828 | 0.9914 | 0.9828 |
| **Cluster** | 0.8475 | 0.9831 | 0.9831 | 0.9746 | 0.9831 |
| **Bootstrap** | 0.9483 | 0.9914 | 0.9741 | 0.9569 | 0.9741 |

---

## 💡 4. Key Takeaways & Conclusion

Looking at the results, a few interesting patterns emerged:

- **Ensemble Methods Rule:** As expected, the tree-based ensemble methods (**Gradient Boosting** and **Random Forest**) consistently dominated across almost all sampling techniques. They are robust and handle this kind of tabular data exceptionally well.
- **The Winning Combo:** The absolute highest accuracy (~**99.35%**) was achieved when combining **Systematic Sampling** with either **Gradient Boosting** or **Random Forest**. It seems the structured spread of systematic sampling provided an excellent representation for these models to learn from.
- **Bootstrapping Helps the Underdog:** Interestingly, **Bootstrap Sampling** provided a massive boost to **Logistic Regression**, bumping its accuracy up to nearly 95%—its best showing across all techniques.
- **Stratified & SVM:** **Stratified sampling** paired surprisingly well with **SVM**, yielding an impressive 99.14% accuracy.

Thanks for checking out the project! Feel free to explore the Jupyter Notebook `sampling_assignment.ipynb` to see the actual code and implementation details.


