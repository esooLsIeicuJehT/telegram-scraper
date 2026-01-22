## 2024-10-18 - CLI Async Feedback
**Learning:** Users often perceive CLI applications as "hung" during silent asynchronous operations, such as parallel network requests.
**Action:** Always wrap long-running blocking calls (like `loop.run_until_complete`) with a visual feedback indicator, such as a thread-based spinner, to provide immediate system status visibility.
