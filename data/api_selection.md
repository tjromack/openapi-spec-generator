# Selected APIs for OpenAPI Spec Generator

## Overview
This document lists the APIs selected for building our golden test set and evaluating the OpenAPI spec generator.

## Selection Criteria
- ✓ Excellent documentation
- ✓ Existing OpenAPI specs available (for validation)
- ✓ Free tier access
- ✓ Variety in complexity
- ✓ Well-maintained and stable

---

## Primary APIs (Build golden set from these)

### 1. JSONPlaceholder (Starter - Simple)
- **URL**: https://jsonplaceholder.typicode.com/
- **Documentation**: https://jsonplaceholder.typicode.com/guide/
- **Why Selected**: Simple REST API, perfect for testing eval harness
- **Complexity**: Low (10 endpoints, basic CRUD operations)
- **Authentication**: None required
- **Rate Limits**: None
- **Golden Set Target**: 5 endpoints
- **Setup Required**: No signup needed
- **Status**: ✓ Accessible and tested

**Key Endpoints for Golden Set:**
- GET /posts
- GET /posts/{id}
- POST /posts
- GET /users
- GET /comments

---

### 2. OpenWeatherMap (Simple)
- **URL**: https://openweathermap.org/api
- **Documentation**: https://openweathermap.org/current
- **Why Selected**: Real-world API with query parameters, good for testing parameter handling
- **Complexity**: Low-Medium (weather data endpoints with various query options)
- **Authentication**: API key (free tier)
- **Rate Limits**: 1,000 calls/day (free tier)
- **Golden Set Target**: 3-4 endpoints
- **Setup Required**: Sign up for free account
- **Status**: ✓ API key configured

**Key Endpoints for Golden Set:**
- GET /data/2.5/weather (current weather by city)
- GET /data/2.5/weather (current weather by coordinates)
- GET /data/2.5/forecast (5 day forecast)

---

### 3. GitHub API (Medium Complexity)
- **URL**: https://docs.github.com/en/rest
- **Documentation**: https://docs.github.com/en/rest/overview
- **Existing OpenAPI Spec**: https://github.com/github/rest-api-description
- **Why Selected**: Excellent documentation, complex nested schemas, industry standard
- **Complexity**: Medium (repos, users, issues with nested objects)
- **Authentication**: Personal Access Token (optional for public endpoints)
- **Rate Limits**: 60 requests/hour (unauthenticated), 5,000/hour (authenticated)
- **Golden Set Target**: 5-6 endpoints
- **Setup Required**: Optional token for higher rate limits
- **Status**: ✓ Token configured

**Key Endpoints for Golden Set:**
- GET /users/{username}
- GET /repos/{owner}/{repo}
- GET /repos/{owner}/{repo}/issues
- GET /repos/{owner}/{repo}/commits
- POST /repos/{owner}/{repo}/issues

---

### 4. SendGrid API (Medium-Complex)
- **URL**: https://www.twilio.com/docs/sendgrid/api-reference
- **Documentation**: https://docs.sendgrid.com/api-reference/
- **Why Selected**: Email service API, nested objects, good variety of operations
- **Complexity**: Medium (mail send, contacts, templates with complex request bodies)
- **Authentication**: API key
- **Rate Limits**: 100 emails/day (free tier)
- **Golden Set Target**: 3-4 endpoints
- **Setup Required**: Sign up for free SendGrid account
- **Status**: ○ Optional - can add later in Phase 1

**Key Endpoints for Golden Set (if used):**
- POST /v3/mail/send
- GET /v3/templates
- POST /v3/contactdb/recipients
- GET /v3/suppression/bounces

---

### 5. Stripe API (Complex - Stretch Goal)
- **URL**: https://stripe.com/docs/api
- **Documentation**: https://stripe.com/docs/api
- **Existing OpenAPI Spec**: https://github.com/stripe/openapi
- **Why Selected**: Gold standard API design, highly complex schemas, excellent docs
- **Complexity**: High (charges, customers, subscriptions with deeply nested objects)
- **Authentication**: API key (test mode)
- **Rate Limits**: Unlimited (test mode)
- **Golden Set Target**: 3-4 endpoints
- **Setup Required**: Sign up for free Stripe account (test mode)
- **Status**: ○ Optional - stretch goal for Phase 1

**Key Endpoints for Golden Set (if used):**
- POST /v1/charges
- GET /v1/customers/{id}
- POST /v1/customers
- GET /v1/subscriptions

---

## Golden Test Set Summary

### Phase 1 Priority (Must Have):
1. **JSONPlaceholder** - 5 endpoints (simple, no auth)
2. **OpenWeatherMap** - 3-4 endpoints (simple API key auth)
3. **GitHub** - 5-6 endpoints (medium complexity)

**Total Priority Set**: 13-15 endpoints

### Phase 1 Optional (If Time Permits):
4. **SendGrid** - 3-4 endpoints
5. **Stripe** - 3-4 endpoints

**Total with Optional**: 19-23 endpoints

---

## Implementation Order

### Week 1 (Phase 1, Part 1):
- JSONPlaceholder (all 5 endpoints)
- OpenWeatherMap (3-4 endpoints)
- **Goal**: 8-9 hand-verified specs in golden set

### Week 1 (Phase 1, Part 2):
- GitHub (5-6 endpoints)
- **Goal**: 13-15 total specs (minimum viable set)

### Optional Extension:
- SendGrid (if needed for variety)
- Stripe (if time permits)

---

## Access Configuration Status

### ✓ Configured and Working:
- [x] JSONPlaceholder (no auth needed)
- [x] OpenWeatherMap (API key: OPENWEATHER_API_KEY)
- [x] GitHub (token: GITHUB_TOKEN)

### ○ Optional (Not Yet Configured):
- [ ] SendGrid (would need: SENDGRID_API_KEY)
- [ ] Stripe (would need: STRIPE_TEST_KEY)

---

## Evaluation Criteria

Each API contributes different testing dimensions:

### JSONPlaceholder:
- Simple GET/POST operations
- Basic JSON responses
- No authentication complexity
- Perfect for baseline eval metrics

### OpenWeatherMap:
- Query parameter handling
- API key authentication
- Real-world response structures
- Error handling (invalid city names)

### GitHub:
- Complex nested objects
- Pagination headers
- Rich schema definitions
- Authentication tokens
- Rate limiting

### SendGrid (Optional):
- Complex request bodies
- Multiple content types
- Batch operations
- Email-specific schemas

### Stripe (Optional):
- Deeply nested objects
- Expandable fields
- Idempotency keys
- Complex business logic in schemas

---

## Success Metrics by API

### JSONPlaceholder (Target: 100% accuracy):
- Endpoint coverage: 100%
- Parameter accuracy: 100%
- Response schema accuracy: 100%
- Hallucination rate: 0%

### OpenWeatherMap (Target: >95% accuracy):
- Endpoint coverage: 100%
- Parameter accuracy: >95%
- Response schema accuracy: >90%
- Hallucination rate: <5%

### GitHub (Target: >90% accuracy):
- Endpoint coverage: >95%
- Parameter accuracy: >90%
- Response schema accuracy: >85%
- Hallucination rate: <10%

---

## Notes for Phase 1

- Start with JSONPlaceholder to build eval harness
- Add OpenWeatherMap to test API key auth
- Add GitHub to test complexity
- Optional APIs can be added if we finish early or need more variety
- Focus on quality over quantity - better to have 15 perfect specs than 25 mediocre ones

---

**Last Updated**: 2025-11-01
**Status**: APIs selected and prioritized for Phase 1
**Next Step**: Begin creating golden test set in Phase 1
