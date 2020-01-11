# Decred Fundamental Metrics Research Proposal - Phase 2
*Checkmate - 30 January 2019*

## Proposal Overview

The Pi proposal is a continuation from Phase 1 and represents ongoing research into the fundamentals and performance metrics of the Decred blockchain. At its core, this research aims to distill the intricacies and details of blockchain analysis and Decred design and diseminate it to a wide audience in easily digestable formats.

The proposed research (as for Phase 1) is primarily targeted at two groups:
- General cryptocurrency enthusiasts/investors who are seeking to learn more about Decred as a protocol and DCR as an asset.

- Institutional Investors by providing sound, detailed and evidence based research supporting an investment thesis.

In short this proposal covers the following two billable categories.
- Pull Requests and coordination to integrate select metrics developed in Phase 1 and by PermabullNino into dcrdata charts.
- Continued data driven analysis and fundamental research into Decred performance

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

***Non-billable but associated work representing Decred***

- Monthly contributer to the [Our Network](https://ournetwork.substack.com/p/our-network-issue-2) newsletter focused on on-chain performance from across the industry.
- Featured on the [Decred in Depth podcast](https://www.youtube.com/watch?v=2JbMWgJUoSQ)
- Featured on the [POV Crypto podcast](https://www.youtube.com/watch?v=7m1kfM0fqaE)

## What
**Integration of charts into dcrdata**

Numerous community requests have come in to integrate Decred metrics developed by myself and PermabullNino into dcrdata charts. This will make live charts available for community inspection and use. The following metrics are proposed to be specified and integrated:
- Block subsidy models by Permabull Nino ([USD](https://miro.medium.com/max/1844/1*sK7IGFqiQ5Nrf831BhEUfQ.png) and [BTC](https://miro.medium.com/max/1843/1*tYb0fdLtJY9PqcGyhFuT6Q.png))
- [Realised Cap, Realised Price and 142-Day Cap](https://miro.medium.com/max/1510/1*NpMJNsSxkPaZP5aHBhml2A.png)
- [142-Day](https://miro.medium.com/max/1522/1*CreqBtFHjLTuuhUDB-WeAg.png) and [28-Day](https://miro.medium.com/max/1545/1*OcPCpGF_U2h4weaSA3KRXw.png) Hodler Conversion rates]
- Cumulative Cap, Hodlers Cap, Participants Cap for [USD](https://miro.medium.com/max/1636/1*QLQfPaduSrcyR3U4beQx0w.png) and [BTC](https://miro.medium.com/max/1631/1*wTMJgilQsWE54qT_Yo2SUw.png)
- Ticket Pool Volume Weighted Price (TVWAP) oscillators for [14-Day](https://miro.medium.com/max/1549/1*dKnx7iW6x_pUdgmcghYRBQ.png), [28-Day](https://miro.medium.com/max/1334/1*ktIRbXlz0mtjZbIfk1o6yA.png) and [142-Day](https://miro.medium.com/max/1506/1*qYVwBqf6Hb98f7QyeNdu-g.png)
- [Cumulative Unforgeable costliness](https://miro.medium.com/max/1280/1*SA8wYN3TUC7CqunFnUR3Yg.png)
- [Daily Finality/Security Budget](https://miro.medium.com/max/1449/1*GQIeyHj1yGeqNdZcU8mxmw.png)
- [Difficulty Ribbon](https://github.com/checkmatey/checkonchain/blob/master/research_articles/our_network_articles/week1_20191225/images/insight_3.png?raw=true)
- Stock-to-Flow [Model](https://miro.medium.com/max/1150/1*6bectH0xB7QfNoFDrDx5Hw.png) and [Multiple](https://miro.medium.com/max/1304/1*WeRtp2iWPaZDfKQDDQqxtg.png) - This one will be coded up but not released until additional statistical checks and validation is completed.

**Phase 2 Research Topics**

This Phase intends to extend both the depth and breadth of research into a number of areas both data driven and more philosophical in nature. Research phase 2 plans to explore the following topics:

*Data Driven Analysis*
- Continued analysis of Decred performance with increased granularity
- Analysis on the break-down of transaction types (tickets, privacy mixes, regular Tx)
- Analysis of supply distribution over time and the implications on security and equity metrics (like gini coefficients etc)
- Developing additional pricing models based on available data and performance

*Armchair Philosophy*
- How Decred and Bitcoin compete for investment and mind share and co-exist as digital SoVs
- Risks, checks and balances and trade-offs made by the Decred blockchain design.
- Comparison between the Bitcoin 'consensus by upgrade' and Decred 'upgrade by consensus' governance models.
- Decred as a digital cypher-punk / Crypto anarchic society.

## Who
dcrdata integration - RichardRed, PermabullNino and myself will work towards this. I anticipate assistance from dcrdata devs however intend to up-skill 
Research - this will be primarily conducted by myself.
