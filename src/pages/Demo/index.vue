<template>
  <div class="">
    <el-container>
      <el-aside width="200px"><Menu /></el-aside>
      <el-main style="width: 100%; padding: 50px 50px 0 50px"><contentIndex /></el-main>
    </el-container>
  </div>
</template>

<script>
import Menu from "../../components/menu/index";
import contentIndex from "../../components/content/index";
export default {
  name: "",
  props: [""],
  data() {
    return {};
  },
  components: {
    contentIndex,
    Menu,
  },
  computed: {},
  mounted() {},
  methods: {},
  watch: {},
};
</script>
<style lang="scss">
@import "./index";
</style>
