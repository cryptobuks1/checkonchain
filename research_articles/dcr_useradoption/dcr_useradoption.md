# Decred, The Resilient Stronghold
*by Checkmate*

*30-Jan-2020*

**Decred** is one of the most promising cryptocurrency projects and a sound competitor next to Bitcoin in the free market for scarce digital money. At a minimum, strong market competition forces innovation and hardening of the strongest protocols whilst also providing a rational hedge for risk during the nascent development of digital money.

The following article is the final part of a three-part study into Decred from a data-driven and first principles perspective. The series aims to critically compare the performance of both Decred and Bitcoin across the following value metrics:

1. [Monetary policy and Scarcity](https://medium.com/@_Checkmatey_/monetary-premiums-can-altcoins-compete-with-bitcoin-54c97a92c6d4)
2. [Cost of Security and Unforgeable Costliness](https://medium.com/@_Checkmatey_/decred-hypersecure-unforgeably-scarce-e076b91a2be)
3. Governance, User Adoption, and Resilience (this paper)

![Decred Cover](images/image_cover.png)
[*Background image courtesy of NASA*](https://www.nasa.gov/sites/default/files/styles/full_width_feature/public/thumbnails/image/iss052e007857.jpg)

# Overview

In this paper, I explore the **resilience, adoption and aggregate behaviour**  of key participants in the Decred network. Decred's incentive structure is unique amongst cryptocurrency protocols, engaging the attention and action of four parties, each with a critical role in sustaining network health:

- **Users** who utilise DCR as an uncensorable and self-sovereign means for storing and transferring wealth.

- **Proof-of-Work Miners** who provide unforgeable ledger security and construction of the blockchain.

- **Proof-of-Stake Stakeholders** who provide checks and balances to PoW security and protocol governance decisions.

- **Proof-of-Skill and Time Builders** who develop, research and disseminate technology, knowledge and awareness to enhance the Decred value stack.

## Skin-in-the-Game

In many instances, individuals participating in the Decred network are active in more than one of these categories, in some cases all four. 

It is not uncommon for Miners, who have invested heavily in both CAPEX and OPEX to compete with ASIC hardware, to take an active interest in governance decisions to protect their investment. This also provides a passive, income stream for mined coins whilst hodling, enabling unique revenue models.

The people who contribute to and develop the Decred codebase, market presence and research base, are typically strong hand holders of DCR and active participants in Proof-of-Stake security and governance. Having developed sound understanding of Decred fundamentals, these people are often motivated and dedicated DCR hodlers of last resort.

These examples are distillations of an essential yet informal value of Decred holders, skin-in-the-game. The Decred design is centred around the fundamentally crypto-anarchic principles of action and accountability of the system whilst preserving the individual's privacy and anonymity. 

> Decred is a crypto-anarchic society. 
> The whole is stronger than the sum of it's parts.
> Yet it protects, secures and obscures each at an individual level.

This paper studies this aggregate behaviour driven by individal skin-in-the-game for all four user categories. It aims to describe how the **Decred** blockchain has performed as a whole over time.

## TL; DR
- X

- X

- X

## Disclosure

*This paper was written and researched as part of the author's [research proposal](https://proposals.decred.org/proposals/78b50f218106f5de40f9bd7f604b048da168f2afbec32c8662722b70d62e4d36) accepted by the Decred DAO. Thus, the writer was paid in DCR for their billed time undertaking the research. Nevertheless, the study aims to be objective and mathematically rigorous based on publicly available market and blockchain data. All findings can be readily verified by readers in the attached [spreadsheet](X) and all assumptions shall be clearly stated.*

# UPDATE SPREADSHEET




# 1) The Immutable Wealth of DCR Holders

At it's core, Decred aims to provide an immutable, uncensorable and self-sovereign store of value in the DCR crypto-asset. Decred's hard-coded, supply cap and deterministic monetary policy make it a valid contender in the landscape of digital stores of value. 

With growing market size and increasing network decentralisation, Decred now boasts an impressive security system. This provides users with a set of unique [assurances for resistance against ledger tampering, block re-organisations and double spends](https://medium.com/@permabullnino/introduction-to-crypto-accounting-an-analysis-of-decred-as-an-accounting-system-4d3e67fce28). Decred's Hybrid PoW/PoS consensus mechanism thus acts to secure user wealth held in DCR, settle value transferred over the ledger and uphold these immutable characteristics.

## Resistance to Reorganisations

The Decred protocol is four years old and impressively has experienced very few blockchain reogranisations through history. Re-organisations to a depth of one block are natural phenomena  in blockchains (including Bitcoin) as a result of network latency and probability and usually work themselves out. As of block height 414,977, the following [block re-orgs have been detected](https://matrix.to/#/!vGasNHFXqjoEWUBTIi:decred.org/$157910732378277MwoqT:decred.org?via=decred.org&via=matrix.org&via=zettaport.com) with the majority of depth 2 and all of depth 3 being associated with a [bug encountered during the DCP004 upgrade](https://matheusd.com/post/dcp0004-and-hardforks/):

- Depth 1 blocks = 1922 instances (0.4631%, natural phenomena).
- Depth 2 blocks = 25 (0.006%, most during DCP004 upgrade).
- Depth 3 blocks = 3 (0.0007%, all during DCP004 upgrade).
- Depth >3 blocks = Nil.

Thus, Decred's implementation of a hybrid PoW/PoS consensus mechanism has to date maintained consensus at the chain tip for 99.9933% of its four year lifespan, impressive for a network valued at $150M at the time of writing.

## Global Transaction Settlement

Decred has settled over $11.44Bil in USD denominated transaction value, via the transfer of 409 Million units of DCR. Of this, $5.55Bil (48%) can be attributed to stakeholders participating in the PoS Ticket system. Tickets represent an active participation mechanism for those holding DCR coins as an inflation hedge, store of value or speculative investment.

For context, Bitcoin at age 4yrs (first halving), had settled a total transaction value of $10.83Bil in USD value via the transfer of 1.17Bil BTC. 

It is worth highlighting some differences in market and coin holding behaviour between Bitcoin and Decred users to detail these observations. 
- Bitcoin pricing and first exchanges became reliably active in 2010-11 before which BTC had no market value. Decred launched into a 2016 market into almost immediate exchange listings to facilitate price discovery.
- For Bitcoin, coins held as a store of value or inflation hedge are often held in cold storage for months to years without transacting, leaving only the withdrawal transaction signature on-chain. Conversely, DCR held by long term holders is in constant on-chain circulation for participation in the PoS ticket system.
- Bitcoin has historically acted as the reserve asset for the cryptocurrency market which increases coin velocity.

Thus, it is reasonable to expect Bitcoin to have settled a higher number of coins (low early price) for a similar aggregate USD value. This data suggests that holding DCR as a long term speculative investment or store of value is the primary use case of DCR to date.

![user_settled.png](images/user_settled.png)

## Daily Transaction Settlement

The transaction value settled by Bitcoin and Decred on a daily basis are shown in the chart below, compared to the most adverse security budget curves developed in [Part 2 of this study](https://medium.com/@_Checkmatey_/decred-hypersecure-unforgeably-scarce-e076b91a2be). It can be seen that both protocols settle millions in USD denominated value, and orders of magnitude more than their respective security budgets. 

This suggests that both protocols display a strong **Settlement Premium** where the value settled exceeds the block reward available as incentivise honest security providers. It is likely this premium is representative of the secondary costs of aquiring hardware, hash-power and coordinating the logistics of an attack. Additionally, one must consider the scope of potential reward for an attacker such as censoring specific transactions, shorting the coin price for profit or system wide disruption (mining empty block etc).

For Decred, the $6.8M in value settled daily aligns approximately with the 15% ticket share security line. In other words, the cost to re-organise the Decred ledger in a double spend attack, assuming the attacker holds 15% of all tickets (at no cost), is approximately equal to the total value flowing through on the chain. Interestingly, this aligns with a typical ticket share of the [largest stakepool](https://decred.org/vsp/). However, this likely consequential rather than a driving factor as this attack vector requires approximately 40x the honest hashpower to conduct and is thus unlikely.

The Decred 50% ticket security curve (light red) can be considered as an equivalent pure PoW security metric as an attacker with 50% of tickets still requires a 51% attack on miners. It can be seen that the **Settlement Premium** is similar in magnitide to 4year old Bitcoin through comparing y-axis values of security curves to daily settled value.

![user_security.png](images/user_security.png)

## User Activity 
Where a notable difference between user behaviour can be observed is via monitoring transaction counts as a proxy for network activity. 

Bitcoin has seen a consistent growth in meaningful transaction counts over time. Transaction counts generally follow/lead movements in price and align with Bitcoin's continued market dominance and position as a local reserve asset for the market.

For Decred, it can be seen that transaction counts have been comparatively higher in the early years however have remained consistent and rangebound throughout its lifetime. This indicates sluggish growth in new users and this trend can be observed across similar activity metrics like active addresses. Decred activity metrics also followed price during the 2016-17 bull market however with a notably weaker correlation strength to Bitcoin.

A consistent baseline of DCR ticket activity makes up around 62% of the cumulative transaction count. This chart shows the aggregate for the three separate transactions through the ticket lifecycle: 1) UTXO aggregation 2) ticket purchase transaction and 3) vote transaction.

Since August 2019, the Decred on-chain privacy mixing protocol has been operational and was followed by an uptick in both transaction counts and active addresses. This is a result of both demand for privacy mixing as well as technical factors whereby mixes utilise more transactions and addresses during execution.

Comparing the count of daily active addresses for both ledgers shows Decred address activity to be around 45% to 50% of that seen for Bitcoin following launch of the privacy implementation. Prior to privacy mixing, Decred was at a low of 25% relative activity.

![user_txcnt.png](images/user_txcnt.png)

## Native Units Moving On-chain

Reviewing the daily mean and median transaction sizes, we can establish a macro view into user behaviour on-chain, and how it has evolved over time. 

Bitcoin's trend shows a gradually reducing mean and median transaction size. This is indicative of the increased economic value supported by the chain following price appreciation through bull-bear cycles. Decred has experienced only once such market cycle (2016-2020). Interestingly, Decred shows a similar magnitude of both mean and median transaction size compared to Bitcoin at the same age.

Decred tickets have experienced a near-linear uptrend in DCR denominated price as more coins enter circulation through the block subsidy. Given an average daily flow of 4,425 ticket related transactions, the ticket price (white) enacts an upwards gravity on both the mean and median transaction sizes.

Mean DCR transaction size has generally followed this ticket price trend closely. Prior to privacy mixing, a mean transaction size of around 80DCR represented 62% of the then ticket price (130DCR), consistent with the cummulative transaction counts metric. Following privacy mixing, an increased volume of smaller sized transactions lead to a decrease in both mean and median size.

The median DCR transaction size has shown an inverse correlation to coin price, a similar trend observed through Bitcoin's history. As the USD value of coins increase, an equivalent denomination of USD value can be stored or transferred in a smaller volume of coins. It is also indicative of increased usage by smaller, retail level users purchasing coins during bullish markets and peaks in market attention. The inverse is also true where bear market users are dominated by larger, long term holders with higher conviction.

![user_local_ntv.png](images/user_local_ntv.png)

## DCR Hodler Summary

Overall, Decred aggregate transactions volume and size suggest comparable economic value flowing through the Decred chain as Bitcoin circa 2013, albeit in fewer, larger sized transactions. Ticket related activity accounts for approximately 50% to 60% of on-chain flows and supports the notion that most users treat DCR as a long term speculative investment or store of value candidate.

Decred has an approximately equal network valuation to Bitcoin at the same age whilst supporting approximately 25% of the daily transaction and active address count (privacy mixing excluded). Along with rangebound transaction counts, this highlights a slower growth and uptake of Decred as well as Bitcoin's dominance as a local reserve asset for the cryptocurrency market. The new CoinJoin implementation clearly indicates strong demand for DCR fungability and Decred block-space, a promising development. 

![user_summary_table.png](images/user_summary_table.png)

# 2) The Unforgeable Work of DCR Miners

Proof-of-Work miners are integral to the security, decentralisation and immutability of the Decred blockchain. Miners are responsible for building the chain through cryptographically hashing valid transactions into blocks before presenting them for validated by PoS tickets.

Miners invest in hardware CAPEX and establish long term energy contracts to provide this service which secured the blockchain through a number of unforgeable mechanisms:

- Creates a financial and logistical hurdle for potential attackers to overcome to aquire sufficient hash-rate and energy to build an competitive side-chain.
- Investment in Application Specific Integrated Circuits (ASICs) create an incentive for honest miners to defend their sunk-cost CAPEX. This aligns miner incentives with the users and success of the Decred blockchain.
- Proof-of-Work roots the cost of block creation to a demand for energy which cannot be forged.
- The globally competitive market for energy leads to widely distributed mining operations in pursuit of favourable combinations of energy sources and contracts, hardware manufacturing, climates and regulatory jurisdictions. This promotes geographical distribution of mining operations to provide system redundancy.

## Growth of Hash-rate

Decred launched into the 2016 market where GPU miners were readily available. Decred thus had an initial difficulty setting equivalent to the hashpower of 256 contemporary GPUs. Decred mining has since progressed to become an ASIC dominated chain as of early 2018 [[1](https://youtu.be/7K2sDhyjQys)], [[2](https://youtu.be/8TPFIVYy_i4)]. Since ASICs have come on-line, the Decred hash-rate has expanded by 1,000x with most growth occuring over a one year period from 2018 to 2019.

The Decred hash-rate currently fluctuates between 400-500 PetaHash/s, similar to that of Bitcoin in 2015. Decred hash-rate has remained relatively stable since early 2019 in response to depression of the DCRUSD price during the bear market cycle.

![miner_pow_growth.png](images/miner_pow_growth.png)

The Decred difficulty ribbon is presented in the chart above by taking a series of daily moving averages (9,14,25,40,60,90,128 and 200 periods) of protocol mining difficulty. The difficulty ribbon provides insight into the aggregate behaviour of miners. This shows that Decred has experienced four distinct phases of the mining cycle throughout its four year lifespan, summarised in the table below.

![miner_character.png](images/miner_character.png)

It can be seen that there are remarkable similarities in the growth rate of hash-power between Decred from year 0 to 4 compared to Bitcoin from year 3 to 6. What is notable is the coupling between Bitcoin price and hash-rate trends. Re-expansion of the Bitcoin difficulty ribbon tends to follow price appreciation during bull markets and, conversely, compresses following the capitulation phase at the end of bear markets.  

For Decred, ASICs were introduced to the network at the peak of what became a significant and industry wide bear market (starting early 2018). Thus Decred has experienced a process of hash-rate expansion due to improved hardware efficiency (supersceding GPUs) without the support of coin price appreciation.

As such, it is likely that the present cohort of ASIC miners have endured challenging financial conditions, particularly through 2019 as seen by the current compression of the Difficulty ribbon as miners turn off unprofitable hardware. Similarly, it is reasonable to conclude that miners will require sustained DCR price appreciation to justify further investment in hardware CAPEX or upgrades.

Assuming a bear market price floor has been found at the time of writing, the Decred hash-rate and mining difficulty will likely remain rangebound at currently levels until this price threshold is passed.

## Miner Income

We can establish a basis for aggregate miner behaviour by reviewing the [cumulative block rewards](https://medium.com/@permabullnino/decred-on-chain-a-look-at-block-subsidies-6f5180932c9b) paid to miners (incl. subsidy and fees). Decred has paid miners over $147M in PoW rewards with $875k of this attributed to transaction fees (0.595%).

Long term development of a fee market is a critical evolution to sustain a fixed maximum coin supply of 21M units. Whilst early in Decred's life, the ratio of daily transaction fees as a proportion of the total block reward shows Decred fees account for 0.04% of miner income. Similar to block-space utility, the Decred privacy implementation has shown a positive feature for miner incomes and the fee ratio.

Of note is the distinct plateau in cumulative transaction fees paid after July 2017. This is a direct result of the consensus rule change to [replace the original stake-difficulty algorithm](https://medium.com/decred/new-stake-difficulty-algorithm-cdf432d623fe) which had a natural resonance in the ticket price. This led to 'fee wars' by users attempting to aquire tickets during price troughs and an overall poor user experience. This consensus rule change [passed a governance vote with 97.9% approval](https://explorer.dcrdata.org/agenda/sdiffalgorithm) despite being clearly against miner short term interest.

There are two mechanisms which would lead to this vote result, both of which the author deems positive outcomes for the Decred project and governance system:

- Miners are freely able to stake mined coins, and during the 2017 bull market, this was a profitable strategy. Thus miners holding tickets still voted in favor of long term user experience rather than in their own short term financial interest. This suggests sound alignment of miner values with those of the rest of the community.
- Mining was dominated by dual Ethereum GPU miners in 2017, whom are generally believed to have distributed DCR coins almost immediately to exchanges for sale. Thus, miners would not have a significant say in the vote and indicates a wide coin distribution into the public has occured which enhances vote decentralisation.

![miner_stakediff.png](images\miner_stakediff.png)

An additional observation pertaining to the cumulative miner rewards paid is the notion of miners 'putting the bottom in' for bear markets. Given this represents the aggregate income of the mining industry, where network valuation falls below this level, it can indicate mining is becoming increasingly unprofitable on aggregate.

This leads to weaker miners disabling mining rigs, a compression of the difficulty ribbon and an increased share of hash-rate gained by stronger miners. Given strong miner stategy tends to focus on accumulation of coins in bullish markets, this begins to constrain the available supply entering the market and has shown to preceed price appreciation and bullish conditions for both Bitcoin and Decred in the past. 

![miner_pow_rewards.png](images/miner_pow_rewards.png)

## Summary of Proof-of-Work Miners

Decred mining is dominated by ASIC hardware and has experienced significant growth in hash-rate despite bear market conditions since 2018. It is likely that miners have been tested by challenging financial conditions and poor profitability as a result which sheds light on mechanisms behind DCR price performance since all-time-highs.

That said, the difficulty ribbon and cumulative rewards paid to miners are exhibiting typical basing patterns seen in other proof-of-work coins like Bitcoin. A notable increase in demand for block-space is seen following the launch of Decred's privacy mixing technology, carrying a net positive impact on the fee ratio and long term sustainability. 

# 3) The Strong Hands of DCR Stakeholders

Long-term holding of DCR is distictly different to many other cryptocurrencies in that it promotes the continual movement of coins in the form of PoS tickets. The purchase of a ticket ([or part thereof](https://docs.decred.org/proof-of-stake/ticket-splitting/)) is an explicit and deliberate act to bind a quantity of the stakeholders DCR coins, in an illiquid state, to the performance of the Decred network.

[Tickets undergo a process](https://docs.decred.org/proof-of-stake/overview/) of maturation, psuedo-random selection to vote and then a delay before coins are released. The whole process can take anywhere between 1.5 and 142days. Ticket stakeholders are thus exposed to coin price volatility and market reaction to any consensus or governance votes during that window.

In reward for their patience, resilience and taking on price risk, stakeholders are rewarded with 30% of the block reward, split between the five tickets selected to vote on each block.

This process gamifies the participation in Decred governance whilst also promoting active participation and a desire to 'choose wisely' for governance and consensus decisions.

## Hodler Psychology

DCR holders are free to opt-out and sell their coins into the market at any time when their coins are not bound in tickets. Thus, all ticket purchases carry an underlying assumption, that the individual believes the ticket price plus block reward will be more valuable in the future than today.

In other words, if a holder believes obtaining the PoS block reward is not worth the volatility risk, they are better off holding liquid DCR coins or to sell them, rather than take on price risk for a psuedo-random period of time.

This is a very different mechanism to Bitcoin holders who will typically move BTC coins they believe to be undervalued into deep cold storage without moving them. The team at [Coinmetrics developed the Realised Price](https://coinmetrics.io/realized-capitalization/) to quantify this behaviour.

The Realised Price measures the aggregate value of each UTXO, priced at the time it last moved. It thus represents an aggregate view on the market cost-basis for BTC coins and a lower bound on what long-term holders believe the Bitcoin network is worth.

For Decred, the realised price is more closely correlated with market value as it is influenced by the continual flow of DCR in tickets. Thus, this metric does not adhere to the same set of assumptions and instead has shown to be a point of market support and resistance in bull and bear markets respectively.

## Stakeholder Commitment

Rational market actors are more likely to sell DCR when they believe coins are overvalued, rather than buy tickets and take on volatility risk. By taking a cumulative sum of all DCR bound in tickets, priced at the time of purchase, we can establish a measure of stakeholder 'commitment' to the Decred chain. This represents the aggregate dollar value locked in tickets.

To date, Decred stakeholders have committed over $5.6 Billion in value to the chain in ticket purchases, approximately 38x the market cap of the entire network at the time of writing.

Interestingly, this psychological stakeholder commitment line has acted as a point of price resistance during the 2017 bull trend. Conversely, PoW miners cannot be expected to commit more hash-power investment than is allowed for in the block reward. The cumulative miner income line has thus shown to be a level of fundamental support during bearish trends.

![staker_cumulative_usd.png](images/staker_cumulative_usd.png)



![staker_cumulative_btc.png](images/staker_cumulative_btc.png)

![staker_ticket_pool.png](images/staker_ticket_pool.png)

# 4) The Skill and Time of DCR Architects






# Builders
At the core of **Decred's** centre of gravity is the network Treasury, fueled by 10% of the block-subsidy. At the time of writing, the treasury has amassed over 650k DCR, equivalent to $11.9M USD. These funds are available for deployment by the hive-mind of stakeholders for the purpose of enhancing **Decred** protcol value. 

The treasury is a invaluable differentiator for Decred. It creates an open, fair and equitable way for individuals to aquire coins by levergaging the whole range of human skills and capabilities. Protocols secured by a pure PoW or PoS consensus model rely on users aquiring coins via technically challenging and expensive mining and/or purchasing off the market.




















## The Cost of Time
A feature where **Decred** differs significantly from the design of **Bitcoin** is in the allocation of 10% of the block subsidy to a network treasury. This capital may be allocated by **Decred** ticket holders towards furthering the project goals and development in an autonomous and self-sustaining manner.

This mechanism carries a number of notable advantages, especially in the long term:

1. **Maximising the protocol's self-sovereignty** via minimising the influence of external parties on project direction. Pure PoW or PoS cryptocurrencies to date have resorted to funding mechanisms such as venture capital raises, initial coin offerings and reliance on donations, all of which have associated constraints such competing ideologies and motivations of backers, compliance and registration with securities law, and slowness of progress (on a donation model).

2. **Incentivises sustained engagement by skilled people** who meaningfully contribute to the project. This grows the pool of DCR holders with skin-in-the-game and enhances resilience of the governance model as these builders are personally motivated to see the protocol succed.

3. **Builds resilience in the development progress** where responsible management of treasury funds during 'good times' can subsequently act as a back-up reserve during downturns to ensure continuued progress.

At the time of writing, the **Decred** treasury is [in the process of migrating](https://proposals.decred.org/proposals/c96290a2478d0a1916284438ea2c59a1215fe768a87648d04d45f6b7ecb82c3f) to a fully on-chain wallet custodied by the pool of DCR ticket holders. This iteration in the design essentially nullifies the potential for any individual to access the treasury balance without explicit approval by DCR ticket holders. It is noted that to date no evidence of treasury fund misappropriation has been observed on the public ledger.
