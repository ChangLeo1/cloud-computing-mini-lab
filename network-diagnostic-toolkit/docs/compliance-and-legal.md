# Australian Compliance / Legal Operating Notes

This page is practical project guidance, **not legal advice**.

## 1. Authorisation is mandatory
Australia's Criminal Code Act 1995 contains computer offences relating to unauthorised access/modification of restricted data and unauthorised impairment of electronic communications/data. This toolkit is deliberately scoped to ordinary diagnostics and should be used only where the operator owns the system or has explicit authority.

Official source:
- https://www.legislation.gov.au/C2004A04868/latest/text

## 2. Privacy and security of reports
Where the Privacy Act/Australian Privacy Principles apply, APP 11 requires reasonable steps to protect personal information from misuse, interference, loss and unauthorised access/modification/disclosure, and reasonable steps to destroy or de-identify information when no longer needed (subject to exceptions).

Official source:
- https://www.oaic.gov.au/privacy/australian-privacy-principles/australian-privacy-principles-guidelines/chapter-11-app-11-security-of-personal-information

If an organisation is subject to the Notifiable Data Breaches scheme, eligible breaches can trigger assessment/notification obligations.

Official source:
- https://www.oaic.gov.au/privacy/notifiable-data-breaches

## 3. Essential Eight
ASD/ACSC recommends the Essential Eight as a baseline set of cyber security mitigation strategies. Small-business guidance recommends starting with MFA, software updates and backups, and then progressing toward Essential Eight Maturity Level One where appropriate.

This toolkit's `--security` output is **only a local posture hint**. It does not certify Essential Eight compliance.

Official sources:
- https://www.cyber.gov.au/business-government/asds-cyber-security-frameworks/essential-eight
- https://www.cyber.gov.au/business-government/small-business-cyber-security/small-business-hub/small-business-cyber-security-guide

## 4. Paid IT support and Australian Consumer Law
Consumer guarantees can apply to services, including due care and skill, fitness for a stated purpose in applicable cases, and supply within a reasonable time when no time is agreed. Do not advertise "guaranteed fix" claims you cannot substantiate, and do not assume a generic "no liability" sentence removes statutory rights.

Official source:
- https://www.accc.gov.au/consumers/buying-products-and-services/consumer-rights-and-guarantees

## 5. Operating checklist for client work
1. Define scope and authorised assets in writing.
2. Identify whether any change action is approved before running it.
3. Use the least intrusive diagnostic step first.
4. Use `--redact` for any report leaving the support channel or being used as a portfolio example.
5. Store client reports securely and delete/de-identify them when no longer needed.
6. Escalate suspected security incidents or data exposure to the client rather than expanding the investigation beyond your authority.
