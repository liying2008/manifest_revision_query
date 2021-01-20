<template>
  <el-dialog
    id="help-container"
    width="60%"
    title="网站帮助"
    :visible.sync="dialogVisible"
    :before-close="handleClose"
  >
    <el-row :gutter="24">
      <el-col :span="12">
        <el-card class="box-card">
          <div
            slot="header"
            class="clearfix"
          >
            <span>快捷键</span>
          </div>
          <div class="text item">
            <p><kbd>p</kbd> : 光标快速定位到 <code>Project/Path</code> 输入框 </p>
            <p><kbd>m</kbd> : 光标快速定位到 <code>Manifest/Revision</code> 输入框 </p>
            <p><kbd>Enter</kbd> : 搜索 </p>
            <p><kbd>?</kbd> ( <kbd>shift + /</kbd> ) : 打开“网站帮助”</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div
            slot="header"
            class="clearfix"
          >
            <span>快捷操作</span>
          </div>
          <div class="text item">
            <p><strong>双击 Manifest File 单元格</strong> : 快速搜索该 <code>Manifest File</code></p>
            <p><strong>双击 Project 单元格</strong> : 快速搜索该 <code>Project</code></p>
            <p><strong>双击 Path 单元格</strong> : 快速搜索该 <code>Path</code></p>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <span
      slot="footer"
      class="dialog-footer"
    >Version: {{thisPackage.version}} | Author: {{thisPackage.author}} |
      View source: <a
        :href="thisPackage.git"
        target="_blank"
      >GitHub</a></span>
  </el-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Help extends Vue {
  @Prop({ default: false, type: Boolean }) private show!: boolean;
  private thisPackage = require('../../package.json');

  private get dialogVisible() {
    return this.show;
  }

  private handleClose() {
    this.$emit('closeDialog');
  }
}
</script>

<style lang="stylus">
#help-container {
  .el-dialog__body {
    padding: 20px 32px;
  }

  .text {
    font-size: 14px;
  }

  .clearfix:before, .clearfix:after {
    display: table;
    content: '';
    clear: both;
  }

  .box-card {
    width: 100%;
  }

  kbd {
    display: inline-block;
    font: 11px 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
    padding: 3px 5px;
    line-height: 10px;
    color: #444d56;
    vertical-align: middle;
    background-color: #fafbfc;
    border: solid 1px #c6cbd1;
    border-bottom-color: #959da5;
    border-radius: 3px;
    box-shadow: inset 0 -1px 0 #959da5;
  }

  .dialog-footer {
    color: #afb4bf;
    font-size: 0.8em;

    a {
      color: #afb4bf;
      font-size: 0.8em;
    }
  }

  code {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(27, 31, 35, 0.05);
    border-radius: 3px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace;
  }
}
</style>
