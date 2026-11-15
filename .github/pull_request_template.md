## What changed
<!-- One or two sentences -->

Closes #<issue number>

## Developer checklist
- [ ] Deployed to my dev target and ran the job
- [ ] Added or updated unit tests

## Tester checklist
<!-- Tester: wait for the deploy-test check to go green, then check these in Databricks -->
- [ ] The `[test] orders_summary` job run succeeded (Jobs & Pipelines)
- [ ] `SELECT * FROM orders_test.sales.orders_summary` shows the expected rows
- [ ] The numbers match the ticket's acceptance criteria
- [ ] Nothing else in the `orders_test` catalog changed unexpectedly
