# Decred Fundamental Metrics Research Proposal - Phase 2
*Checkmate - 30 January 2019*

## Proposal Overview

This Pi proposal is a continuation from Phase 1 and represents ongoing research into the fundamentals and performance metrics of the Decred blockchain. At its core, this research aims to distill the intricacies and details of blockchain analysis and Decred design, and diseminate it to a wide audience in easily digestable formats.

The proposed research is primarily targeted at two groups:
- General cryptocurrency enthusiasts/investors who are seeking to learn more about Decred as a protocol and DCR as an asset.

- Institutional Investors by providing sound, detailed and evidence based research supporting an investment thesis.

In short this proposal covers the following two billable categories.
- Developing Git Issues for dcrdata with specific requirements for integrating a set of metrics developed by myself and PermabullNino into dcrdata charts.
- Continued data driven analysis and fundamental research into Decred performance with deliverable papers and social dissemination.

## Review of Phase 1 Deliverables

The goals and objectives and delivered outcomes from Phase 1:

***Goal 1+2: Research articles focused on Decred security, scarcity and SoV characteristics from a first principles perspective.***

Four papers were delivered (first in arrears)
- [Monetary premiums, can altcoins compete with Bitcoin](https://medium.com/@_Checkmatey_/monetary-premiums-can-altcoins-compete-with-bitcoin-54c97a92c6d4) - preliminary study establishing Decred as a potential digital SoV candidate.
- [Decred, Following in Bitcoin's Footsteps](https://medium.com/@_Checkmatey_/decred-following-in-bitcoins-footsteps-f8d0e0bbaff5) - focused on monetary policy, scarcity and built a framework for a potential stock-to-flow type model of value.
- [Decred, Hyper-secure, Unforgably Scarce](https://medium.com/@_Checkmatey_/decred-hypersecure-unforgeably-scarce-e076b91a2be) - focused on contextualising the Decred pre-mine, analysing the unforgeable costliness and quantifying the chains security budget and finality.
- [Decred, Reviewing the Performance of a Cyper-punk Society]() - focused on establishing the performance of the three Decred stakeholders, miners, users/stakers and builders.

***Goal 3+4: Establishing an enhanced level of community engagement and momentum via social media***

All delivered papers were been supported by dissemination of insights via Twitter and Reddit posts. Twitter account is ~90% focused on Decred related content with typical monthly impressions ranging 750k to 1M and growing from 500 to 1850 over the course of Phase 1.

Anecdotally speaking, there appears to be renewed vigour around the Decred project that has attained sound momentum. This is the result of a concerted effort from contractors (incl. Ditto) and the community and I hope to have played at least some role in this.

***Non-billable but associated work***

- Monthly contributer to the [Our Network](https://ournetwork.substack.com/p/our-network-issue-2) newsletter focused on on-chain performance from across the industry.
- Featured on the [Decred in Depth podcast](https://www.youtube.com/watch?v=2JbMWgJUoSQ)
- Featured on the [POV Crypto podcast](https://www.youtube.com/watch?v=7m1kfM0fqaE)
- Accomplished personal goal of learning python data science --> next step is disecting dcrdata.

## What
**Specification of charts to be added into dcrdata**

Numerous community members have requested integration of Decred on-chain metrics developed by myself and PermabullNino into dcrdata charts. This will make live charts available for community inspection and use.

This proposal only covers specification of the required data, calculations and chart layouts and writing into Git Issues. In coversation with @chappjc, the integration with dcrdata is best done by dcrdata devs incrementally potentially via a separate proposal once technical requirements are better understood.

The following metrics are proposed to be specified:
- Block subsidy models by Permabull Nino ([USD](https://miro.medium.com/max/1844/1*sK7IGFqiQ5Nrf831BhEUfQ.png) and [BTC](https://miro.medium.com/max/1843/1*tYb0fdLtJY9PqcGyhFuT6Q.png))
- [Realised Cap, Realised Price and 142-Day Cap](https://miro.medium.com/max/1510/1*NpMJNsSxkPaZP5aHBhml2A.png)
- Cumulative Cap, Hodlers Cap, Participants Cap for [USD](https://miro.medium.com/max/1636/1*QLQfPaduSrcyR3U4beQx0w.png) and [BTC](https://miro.medium.com/max/1631/1*wTMJgilQsWE54qT_Yo2SUw.png)
- [142-Day](https://miro.medium.com/max/1522/1*CreqBtFHjLTuuhUDB-WeAg.png) and [28-Day](https://miro.medium.com/max/1545/1*OcPCpGF_U2h4weaSA3KRXw.png) Hodler Conversion rates
- Ticket Pool Volume Weighted Price (TVWAP) oscillators for [14-Day](https://miro.medium.com/max/1549/1*dKnx7iW6x_pUdgmcghYRBQ.png), [28-Day](https://miro.medium.com/max/1334/1*ktIRbXlz0mtjZbIfk1o6yA.png) and [142-Day](https://miro.medium.com/max/1506/1*qYVwBqf6Hb98f7QyeNdu-g.png)
- [Cumulative Unforgeable costliness](https://miro.medium.com/max/1280/1*SA8wYN3TUC7CqunFnUR3Yg.png)
- [Daily Finality/Security Budget](https://miro.medium.com/max/1449/1*GQIeyHj1yGeqNdZcU8mxmw.png)
- [Difficulty Ribbon](https://github.com/checkmatey/checkonchain/blob/master/research_articles/our_network_articles/week1_20191225/images/insight_3.png?raw=true)
- Stock-to-Flow [Model](https://miro.medium.com/max/1150/1*6bectH0xB7QfNoFDrDx5Hw.png) and [Multiple](https://miro.medium.com/max/1304/1*WeRtp2iWPaZDfKQDDQqxtg.png) - This one will be spec-ed up but not released until additional statistical checks, rigor and validation are completed given it is a forward looking metric.

All future metrics developed during research will include a git issue to streamline this process, thus this is a bring up to speed proposal.

*I call for community commentary on how it is best envisioned to present these metrics (i.e. separate section of dcrdata, new spin off website etc). It is desireable to have a small blurb and link to the research paper to ensure clarity on what each metric is showing and how to interpret it, similar to [woobull.com](http://charts.woobull.com/bitcoin-rvt-ratio/)*.

**Phase 2 Research Topics**

This Phase intends to extend both the depth and breadth of research into a number of areas both data driven and more philosophical in nature. Research phase 2 plans to explore the following topics:

*Data Driven Analysis*
- Continued analysis of Decred performance with increased granularity (intend to explore deeper dcrdata capabilities).
- Analysis on the break-down of transaction types (tickets, privacy mixes, regular Tx).
- Analysis of supply distribution over time and the implications on security and equity metrics (like gini coefficients, cost to attack etc).
- Developing additional pricing models based on available data and performance.
- Statistical verification of the Stock-to-Flow model.
- Review of areas where Decred on-chain performance excels and where it requires attention.

*Armchair Philosophy*
- How Decred and Bitcoin compete for investment and mind share and co-exist as digital SoVs.
- Decred and it's differentiators, how it stands unique in the market.
- Risks, checks and balances and trade-offs made by the Decred blockchain design.
- Comparison between the Bitcoin 'consensus by upgrade' and Decred 'upgrade by consensus' governance models.
- Decred as a digital cypher-punk / Crypto anarchic society.

## Deliverables
1a) dcrdata git issues for metrics above
1b) standard format for delivery of metric specs for faster integration into dcrdata
2a) At minimum 4x detailed research papers of quality similar to those delivered in Phase 1
2b) Continued dissemination of research outcomes and insights via social media channels (Twitter, Reddit, Telegram, Matrix etc)

## Who
**dcrdata specs** - PermabullNino and myself will work towards this. I anticipate ad-hoc input from dcrdata devs however suggest that billable work associated with integration be a separate proposal once metrics are specified and technical/time requirements are better understood.

Research - this will be conducted by myself with usual coordination.

## Timeline
Based on my burn rate from Phase 1, This will represent ~6-8 months of work, accounting for H1 2020. Typical burn rate is $2k to 2.5k/mth as a part time basis.

## Budget Requested
- **1a and 1b = $2,000** for developing specification Git Issues for dcrdata metrics. This includes coordination and establishing a format for all future metrics to adhere to upon delivery.
- **2a and 2b = $14,000** for all research work and dissemination.
- **TOTAL = $16,000**

*Please Note - as part of this proposal work, I will be learning required code skills to extract from dcrdata. As with Phase 1, I do not bill work during the learning curve but do bill work that is directly attributed to research outcomes (i.e. the analysis and developing chart outputs)*

## Risks
The primary risk is time. I consider the 
