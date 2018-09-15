<template>
  <div id="main-container">
    <el-header>
      <el-row class="autocomplete"
              :gutter="40">
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            v-model="project"
            ref="input_project"
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
        ref="main_table"
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
          :filters="revisionFilters"
          :filter-method="filterRevision"
          header-align="center"
          label="Revision"
          width="'25%'">
        </el-table-column>
      </el-table>
    </el-container>
    <el-footer height="30px">
      <div id="footer">
        <span>Data update time: {{dataUpdateTime}}</span>
        <span> | </span>
        <span>Number of manifest files: {{manifestFilesNum}}</span>
        <span> | </span>
        <span>Number of projects: {{projectsNum}}</span>
        <span> | </span>
        <span>Press "?" to view help.</span>
      </div>
    </el-footer>
    <help-dialog
      :show="helpDialogVisible"
      @closeDialog="helpDialogVisible=false">
    </help-dialog>
  </div>
</template>

<script>
  import {LOCAL_STORAGE_SELECT, SEPARATOR} from '@/components/constants';
  import Help from '@/components/Help';

  export default {
    name: 'Main',

    data() {
      return {
        tableHeight: window.innerHeight - 130,
        dataUpdateTime: '1970-01-01 00:00:00',
        manifestFilesNum: '0',
        projectsNum: '0',
        loading: false,
        select: 'project',
        project: '',
        manifest: '',
        projects: [],
        paths: [],
        manifests: [],
        tableData: [],
        helpDialogVisible: false,
        revisionFilters: [],
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
      this.$axios.get('static/projects.list').then((res) => {
        let projects = res.data.split('\n');
        this.projects = projects.map(project => {
          let obj = {};
          obj.value = project;
          return obj
        });
      });
      // path 自动完成列表
      this.$axios.get('static/paths.list').then((res) => {
        let paths = res.data.split('\n');
        this.paths = paths.map(path => {
          let obj = {};
          obj.value = path;
          return obj
        });
      });
      // manifest 自动完成列表
      this.$axios.get('static/manifests.list').then((res) => {
        let manifests = res.data.split('\n');
        this.manifests = manifests.map(manifest => {
          let obj = {};
          obj["value"] = manifest;
          return obj
        });
      });
      // 数据更新时间等信息
      this.$axios.get('static/data_info.json').then((res) => {
        this.dataUpdateTime = res.data.update_time;
        this.manifestFilesNum = res.data.manifest_files_num;
        this.projectsNum = res.data.projects_num;
      });
      // 全局添加按键监听
      document.onkeydown = (event) => {
        return this.keyCheck(event)
      }
    },
    methods: {
      keyCheck(event) {
        // 键盘按键监听处理
        // console.log(event);
        let inputProject = this.$refs.input_project;
        let inputManifest = this.$refs.input_manifest;
        if (this.helpDialogVisible) {
          let key = event.key.toLowerCase();
          if (key !== 'shift' && key !== 'control' && key !== 'alt' && key !== 'contextmenu' &&
            key !== "capslock" && key !== "numlock" && key !== "pause") {
            // 隐藏网站帮助
            this.helpDialogVisible = false;
            return false
          }
        } else {
          if (event.key.toLowerCase() === 'enter') {
            this.search();
            // 让输入框失去焦点
            inputProject.$el.querySelectorAll('input')[1].blur();
            inputManifest.$el.querySelector('input').blur();
            return false
          } else if (event.key.toLowerCase() === 'p') {
            // Project 输入框获取焦点
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              inputProject.focus();
              // 阻止 按键事件继续传递
              return false
            }
          } else if (event.key.toLowerCase() === 'm') {
            // Manifest 输入框获取焦点
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              inputManifest.focus();
              // 阻止 按键事件继续传递
              return false
            }
          } else if (event.key === '?') {
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              // 显示网站帮助
              this.helpDialogVisible = !this.helpDialogVisible;
              return false
            }
          }
        }
        return true
      },
      searchProject(row, column, cell, event) {
        // console.log(row);
        // console.log(column);
        // console.log(cell);
        // console.log(event);
        if (column.property === 'manifest') {
          // 双击的 manifest
          this.manifest = cell.textContent;
          this.project = '';
          this.loadDataFromManifest(false)
        }
        else if (column.property === 'project') {
          // 双击的 project
          this.project = cell.textContent;
          this.select = 'project';
          this.manifest = '';
          this.loadDataFromProject()
        }
        else if (column.property === 'path') {
          // 双击的 path
          this.project = cell.textContent;
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
        this.$axios.get('static/manifests/' + manifest).then((res) => {
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
          this.getRevisionFilters()
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
          url = 'static/projects/' + project
        } else {
          url = 'static/paths/' + project
        }
        this.$axios.get(url).then((res) => {
          // console.log(res.data)
          this.tableData = res.data;
          this.getRevisionFilters()
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
      },

      getRevisionFilters() {
        // 清除过滤
        this.$refs.main_table.clearFilter();
        this.revisionFilters = [];
        let revisionSet = new Set();
        this.tableData.forEach((value) => {
          revisionSet.add(value.revision)
        });
        revisionSet.forEach((value) => {
          let obj = {};
          obj.text = value;
          obj.value = value;
          this.revisionFilters.push(obj)
        });
      },

      filterRevision(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      }
    },
    components: {
      'help-dialog': Help
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #main-container {
    margin: 0 20px 0 20px;
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

  #main-container .el-footer {
    display: flex;
    flex-direction: column;
    -webkit-align-items: center;
    align-items: center;
    -webkit-justify-content: center;
    justify-content: center;
  }

  #main-container #footer {
    font-size: 12px;
    margin: 0;
    padding: 0;
    color: #afb4bf;
  }
</style>
