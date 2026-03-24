# Learnings

This project was primarily an exercise in controlled AI-assisted development, focusing on decision-making, tradeoffs, and maintaining a clear scope.

## 1. Importance of a Specification-First Approach

One of the most important takeaways was the value of defining a clear specification before starting implementation.

Initially, it is tempting to ask the AI to generate code immediately, but this often leads to:

- over-engineered solutions
- unnecessary features
- increased iteration and token usage

By first discussing the problem, defining scope, and creating a `spec.md`, the implementation phase became significantly more efficient and predictable.

---

## 2. Using AI for Decision Support

During the early design phase, I initially considered introducing a database for storing and querying the dataset.

After discussing this with the AI, it highlighted that:

- the dataset size is manageable in memory
- there is no requirement for persistence
- adding a database would increase complexity without clear benefit for this use case

Based on this, I decided to use in-memory processing with pandas.

This reinforced an important lesson:

- AI can be useful not just for generating solutions, but for validating and challenging initial assumptions
- discussing alternatives with AI helps identify unnecessary complexity early

This led to a simpler and more appropriate design for the scope of the assignment.

---

## 3. Tradeoff-Driven Thinking

The project reinforced the importance of making conscious tradeoffs rather than defaulting to standard patterns.

Examples:

- in-memory processing vs database
- App Runner vs ECS + Fargate
- React vs simpler tools like Streamlit

In each case, the goal was not to choose the most scalable or feature-rich option, but the one that best fits the assignment constraints.

---

## 4. Simplicity Over Overengineering

A key learning was that simplicity is often the better engineering choice, especially under time constraints.

I explicitly avoided:

- authentication
- background jobs
- real-time processing
- complex infrastructure

This allowed me to focus on delivering a complete and understandable solution rather than a partially implemented complex system.

---

## 5. Improved Understanding of AWS Services

During the deployment design phase, I explored several AWS services and their tradeoffs:

- App Runner vs ECS + Fargate
- Amplify vs S3 + CloudFront
- storage considerations (e.g. S3 vs other options)

I also created an AWS account to explore these services directly, which helped in understanding:

- how managed services simplify deployment
- when more control (e.g. ECS) is useful vs unnecessary
- how different services fit different use cases

---

## 6. Separation of Concerns in AI-Assisted Development

I learned to separate the development process into distinct phases:

1. problem understanding
2. scope definition
3. specification (`spec.md`)
4. implementation using AI
5. refinement

This structured approach reduced confusion and made the overall workflow more efficient.

---

## 7. What I Would Improve

With more time, I would:

- precompute and cache frequently used aggregations to reduce repeated computation
- introduce a lightweight persistence layer or shared storage for better scalability
- refine the CI/CD pipeline (e.g. full tag-based deployment flow)
- improve frontend UX with additional filtering or interactivity
- move the dataset to S3

---

## Summary

The most important takeaway is:

> Effective AI usage is not about generating code quickly, but about structuring the problem, constraining the solution, and guiding the AI toward the right outcome.

This project reinforced that good engineering decisions come from:

- clear thinking
- controlled scope
- and tradeoffs
