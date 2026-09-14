# Northwind Bank — PoC discovery call

Date: 18 September 2026. Attendees: Dana Osei (Head of Platform, our champion),
Marc Lefevre (DevOps Engineer), Aiko Tanaka (SRE). Datadog: Priya Raman (AE),
Sam Rivera (SE).

## Current state

Logs are split across Splunk (on-prem, expensive) and CloudWatch across three AWS
accounts. No distributed tracing anywhere on the payments path. When a payment
incident happens, engineers open four tools and correlate by hand; Dana said a recent
card-auth outage took 90 minutes just to work out which service was failing.

## What they want

One place to search logs across all three accounts. Tracing on the payments path so
they can see which service degraded. Dana wants to cut the "where is the problem"
phase of incident response, not necessarily the fix time.

## Use cases discussed

1. Unified log search across the three AWS accounts
2. APM and distributed tracing for the payments services
3. Kubernetes monitoring for the EKS clusters

## Environment

EKS 1.29 in eu-west-1, about 40 services. Java 17 / Spring Boot 3.2 for payments,
some Python 3.11 batch jobs. PostgreSQL 15 on RDS. Pre-prod cluster available for the
PoC, owned by Marc. Data residency is EU-only — they were explicit about this.

## Incident data

Dana shared last year's numbers: 64 major incidents, typically 12 people involved,
around 18 hours each. They think unified tooling could cut that to roughly 9 hours.

## Logistics

Twice-weekly cadence suits them, Tuesdays and Thursdays. They use Slack. Target
kick-off 6 October 2026. Showback to the platform and SRE leads at the end.
No RUM — they have no customer-facing web frontend in scope.
