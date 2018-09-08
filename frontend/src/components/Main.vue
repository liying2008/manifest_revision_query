<template>
  <div id="main-container" @keyup.native="keyCheck(event)">
    <el-header>
      <el-row class="autocomplete"
              :gutter="40">
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            v-model="project"
            clearable
            :fetch-suggestions="queryProject"
            :placeholder="projectInputPlaceholder"
            @select="handleSelect">
            <el-select v-model="select" slot="prepend" :value="select">
              <el-option label="Project" value="project"></el-option>
              <el-option label="Path" value="path"></el-option>
            </el-select>
          </el-autocomplete>
        </el-col>
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            clearable
            v-model="manifest"
            ref="input_manifest"
            :fetch-suggestions="queryManifest"
            placeholder="Please enter manifest file name"
            @select="handleSelect">
            <template slot="prepend">Manifest File</template>
          </el-autocomplete>
        </el-col>
        <el-col :span="4">
          <el-button class="inline-button"
                     icon="el-icon-search"
                     @click="search">Search
          </el-button>
        </el-col>
      </el-row>

    </el-header>
    <el-container>
      <el-table
        :data="tableData"
        :height="tableHeight"
        v-loading="loading"
        align="left"
        border
        @cell-dblclick="searchProject"
        highlight-current-row
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index">
        </el-table-column>
        <el-table-column
          prop="manifest"
          sortable
          header-align="center"
          label="Manifest File"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="project"
          sortable
          header-align="center"
          label="Project"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="path"
          sortable
          header-align="center"
          label="Path"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="revision"
          sortable
          header-align="center"
          label="Revision"
          width="'25%'">
        </el-table-column>
      </el-table>
    </el-container>
  </div>
</template>

<script>
  import {LOCAL_STORAGE_SELECT, SEPARATOR} from '@/components/constants';

  export default {
    name: 'Main',

    data() {
      return {
        tableHeight: window.innerHeight - 124,
        loading: false,
        select: 'project',
        project: '',
        manifest: '',
        projects: [],
        paths: [],
        manifests: [],
        tableData: []
      }
    },
    computed: {
      projectInputPlaceholder() {
        if (this.select === 'project') {
          return 'Please enter project name'
        } else {
          return 'Please enter path'
        }
      }
    },
    watch: {
      select: function (newValue, oldValue) {
        // 将用户的选择持久化存储到 Local Storage
        localStorage.setItem(LOCAL_STORAGE_SELECT, newValue);
      }
    },
    mounted() {
      // 从 Local Storage 中读取用户上次的选择
      let select = localStorage.getItem(LOCAL_STORAGE_SELECT);
      if (select === 'project' || select === 'path') {
        this.select = select
      }
      // project 自动完成列表
      this.$axios.get('/static/projects.list').then((res) => {
        let projects = res.data.split('\n');
        this.projects = projects.map(project => {
          let obj = {};
          obj.value = project;
          return obj
        });
      });
      // path 自动完成列表
      this.$axios.get('/static/paths.list').then((res) => {
        let paths = res.data.split('\n');
        this.paths = paths.map(path => {
          let obj = {};
          obj.value = path;
          return obj
        });
      });
      // manifest 自动完成列表
      this.$axios.get('/static/manifests.list').then((res) => {
        let manifests = res.data.split('\n');
        this.manifests = manifests.map(manifest => {
          let obj = {};
          obj["value"] = manifest;
          return obj
        });
      });
      // 全局添加按键监听
      document.onkeydown = (event) => {
        this.keyCheck(event)
      }
    },
    methods: {
      keyCheck(event) {
        // 键盘按键监听处理
        console.log(event);
        if (event.code === 'Enter') {
          this.search()
        } else if (event.code === 'Slash' && event.shiftKey) {
          // 显示网站帮助
        }
      },
      searchProject(row, column, cell, event) {
        // console.log(row);
        // console.log(column);
        // console.log(cell);
        // console.log(event);
        if (column.property === 'manifest') {
          // 双击的 manifest
          let manifest = cell.textContent;
          this.manifest = manifest;
          this.project = '';
          this.loadDataFromManifest(false)
        }
        else if (column.property === 'project') {
          // 双击的 project
          let project = cell.textContent;
          this.project = project;
          this.select = 'project';
          this.manifest = '';
          this.loadDataFromProject()
        }
        else if (column.property === 'path') {
          // 双击的 path
          let path = cell.textContent;
          this.project = path;
          this.select = 'path';
          this.manifest = '';
          this.loadDataFromProject()
        }
      },
      queryProject(queryString, cb) {
        let projects = [];
        if (this.select === 'project') {
          projects = this.projects;
        } else {
          projects = this.paths;
        }
        let results = queryString ? projects.filter(this.createFilter(queryString)) : projects;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      queryManifest(queryString, cb) {
        let manifests = this.manifests;
        let results = queryString ? manifests.filter(this.createFilter(queryString)) : manifests;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
        };
      },
      handleSelect(item) {
        // 点击选中建议项时触发
        // console.log(item);
      },
      loadDataFromManifest(filterProject) {
        let manifest = this.manifest.replace(/\//g, SEPARATOR).trim();
        this.$axios.get('/static/manifests/' + manifest).then((res) => {
          // console.log(res.data)
          if (!filterProject) {
            this.tableData = res.data
          } else {
            this.tableData = res.data.filter((val) => {
              if (this.select === 'project') {
                return val.project === this.project
              } else {
                return val.path === this.project
              }
            });
            if (this.tableData.length === 0) {
              this.$message.error('没有匹配项：' + this.manifest + ' & ' + this.project);
            }
          }
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          this.$message.error('未找到 Manifest 文件：' + this.manifest);
        });
      },

      loadDataFromProject() {
        let project = this.project.replace(/\//g, SEPARATOR, -1).trim();
        console.log(project);
        let url = '';
        if (this.select === 'project') {
          url = '/static/projects/' + project
        } else {
          url = '/static/paths/' + project
        }
        this.$axios.get(url).then((res) => {
          // console.log(res.data)
          this.tableData = res.data
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          if (this.select === 'project') {
            this.$message.error('未找到 Project：' + this.project);
          } else {
            this.$message.error('未找到 Path：' + this.project);
          }
        });
      },

      search() {
        this.loading = true;
        this.project = this.project.trim();
        this.manifest = this.manifest.trim();
        if (this.project === '' && this.manifest === '') {
          this.$message.error('Project/Path 和 Manifest 需要至少填写一项');
        } else if (this.project === '') {
          // manifest 有值
          this.loadDataFromManifest(false)
        } else if (this.manifest === '') {
          // project 有值
          this.loadDataFromProject()
        } else {
          // project 和 manifest 都有值
          this.loadDataFromManifest(true)
        }
        this.loading = false;
      }
    },
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #main-container {
    margin: 20px 26px 26px 20px;
  }

  #main-container .el-header {
    padding: 0;
  }

  #main-container .inline-input {
    width: 100%;
    margin-right: 10px;
  }

  #main-container .inline-button {
    width: 100%;
  }

  #main-container .el-select .el-input {
    width: 130px;
  }

  #main-container .el-table td {
    padding: 8px 0;
  }

  #main-container .el-table th {
    padding: 4px 0;
  }
</style>
