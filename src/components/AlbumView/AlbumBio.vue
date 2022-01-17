<template>
  <div class="al-bio rounded">
    <div class="heading">
      The Very Best Of UB40: ALBUM BIOGRAPHY
      <div class="tags">
        <div class="item" v-for="tag in tags" :key="tag">
          {{ tag }}
        </div>
      </div>
    </div>
    <div class="separator"></div>
    <div class="content">
      Two years after he prematurely left us, the Juice WRLD story continues
      with Fighting Demons. The rapper's second posthumous album dropped at
      midnight, and is the followup to Legends Never Die, which arrived in July
      2020 and hit No. 1 on the Billboard 200 chart.
      <br /><br />
      Featuring the previously-released numbers “Wandered to LA” with Justin
      Bieber, and “Already Dead,” Fighting Demons is a call to arms, a reminder
      for addicts to get help and for those struggling with mental health
      problems to keep up the fight. The rising hip-hop star (real name Jarad
      Higgins) was just 21 when he died of an accidental overdose of oxycodone
      and codeine. Following his death on Dec. 9, 2019, his mother, Carmela
      Wallace, created the Live Free 999 Fund, to help youth struggling with
      mental health and substance use issues.
      <br /><br />
      “Jarad was always searingly honest about his struggles and through his
      musical genius he articulated what was on his heart and mind vividly
      through his art. He never gave up and his friends and family never gave up
      on offering their support to him,” she continued. “We encourage all of you
      who struggle with addiction and mental health to never give up the fight."
      Juice's fast rise in the hip-hop space and untimely passing is the focus
      of Into the Abyss, a Tommy Oliver-directed documentary set to premiere
      Dec. 16 at 8PM on HBO Max.
    </div>
  </div>
</template>

<script>
export default {
  setup() {
    const tags = ["reggea", "ub40", "ali campbell", "astro"];
    return {
      tags,
    };
  },
};
</script>

<style lang="scss">
.al-bio {
  background-color: #1f1e1d;
  padding: $small;

  .heading {
    margin: 0 0 0 $small;
    height: 2rem;
    position: relative;

    .tags {
      position: absolute;
      right: 0;
      display: flex;
      font-weight: normal;

      .item {
        padding: $small;
        background-color: rgb(15, 74, 114);
        margin-left: $small;
        border-radius: $small;
      }
      .item::before {
        content: "#"
      }
    }
  }

  .content {
    display: inline-block;
    line-height: 1.5rem;
    font-size: large;
    columns: 2;
    column-rule: 1px solid $separator;
    font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
    user-select: text;
  }
}
</style>