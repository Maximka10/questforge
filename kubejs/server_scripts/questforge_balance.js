// QuestForge balance layer.
// Keep this file conservative: core progression is controlled by mod recipes,
// while this script only documents the intended balance hooks.

ServerEvents.recipes(event => {
  // Do not globally nerf Create/Mekanism recipes here. The quest tree is the
  // progression gate, while the machines remain useful for sandbox play.
})

ServerEvents.loaded(event => {
  console.info('[QuestForge] balance layer loaded')
})
