<template>
  <div id="main-container">
    <el-header>
      <el-row
        class="autocomplete"
        :gutter="40"
      >
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            clearable
            v-model="project"
            ref="input_project"
            :fetch-suggestions="queryProject"
            :placeholder="projectInputPlaceholder"
            @select="handleSelect"
          >
            <el-select
              v-model="projectSelect"
              slot="prepend"
              :value="projectSelect"
            >
              <el-option
                label="Project"
                value="project"
              ></el-option>
              <el-option
                label="Path"
                value="path"
              ></el-option>
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
            :placeholder="manifestInputPlaceholder"
            @select="handleSelect"
          >
            <el-select
              v-model="manifestSelect"
              slot="prepend"
              :value="manifestSelect"
            >
              <el-option
                label="Manifest"
                value="manifest"
              ></el-option>
              <el-option
                label="Revision"
                value="revision"
              ></el-option>
            </el-select>
          </el-autocomplete>
        </el-col>
        <el-col :span="4">
          <el-button
            class="inline-button"
            icon="el-icon-search"
            @click="search"
          >Search
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
        @cell-dblclick="cellDoubleClick"
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column
          header-align="center"
          type="index"
        >
        </el-table-column>
        <el-table-column
          prop="manifest"
          sortable
          header-align="center"
          label="Manifest File"
          width="'25%'"
        >
        </el-table-column>
        <el-table-column
          prop="project"
          sortable
          header-align="center"
          label="Project"
          width="'25%'"
        >
        </el-table-column>
        <el-table-column
          prop="path"
          sortable
          header-align="center"
          label="Path"
          width="'25%'"
        >
        </el-table-column>
        <el-table-column
          prop="revision"
          sortable
          :filters="revisionFilters"
          :filter-method="filterRevision"
          header-align="center"
          label="Revision"
          width="'25%'"
        >
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
        <span>Number of revisions: {{revisionsNum}}</span>
        <span> | </span>
        <span>Press "?" to view help.</span>
      </div>
    </el-footer>
    <help-dialog
      :show="helpDialogVisible"
      @closeDialog="helpDialogVisible=false"
    >
    </help-dialog>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import Help from '@/views/Help.vue'; // @ is an alias to /src
import { PROJECT_PATH_SELECT, MANIFEST_REVISION_SELECT } from '@/constants/constants';
import { AxiosError, AxiosResponse } from "axios";
import { FilterItem, Value } from "@/entity/commons";
import { DataInfo } from "@/entity/data_info";
import { Data } from "@/entity/data";
import { Autocomplete, Table } from "element-ui";

const SELECT_PROJECT_FLAG = 'project';
const SELECT_PATH_FLAG = 'path';
const SELECT_MANIFEST_FLAG = 'manifest';
const SELECT_REVISION_FLAG = 'revision';

@Component({
  components: {
    'help-dialog': Help,
  },
})
export default class Main extends Vue {
  private tableHeight: number = window.innerHeight - 130;
  private dataUpdateTime: string = '1970-01-01 00:00:00';
  private manifestFilesNum: number = 0;
  private projectsNum: number = 0;
  private revisionsNum: number = 0;
  private loading: boolean = false;
  private projectSelect: string = SELECT_PROJECT_FLAG;
  private manifestSelect: string = SELECT_MANIFEST_FLAG;
  private project: string = '';
  private manifest: string = '';
  private projects: Value<string>[] = [];
  private paths: Value<string>[] = [];
  private manifests: Value<string>[] = [];
  private revisions: Value<string>[] = [];
  private tableData: Data[] = [];
  private helpDialogVisible: boolean = false;
  private revisionFilters: FilterItem[] = [];

  private get projectInputPlaceholder() {
    if (this.projectSelect === SELECT_PROJECT_FLAG) {
      return 'Please enter project name'
    } else {
      return 'Please enter project path'
    }
  }

  private get manifestInputPlaceholder() {
    if (this.manifestSelect === 'manifest') {
      return 'Please enter manifest file name'
    } else {
      return 'Please enter revision'
    }
  }

  @Watch('projectSelect')
  private watchProjectSelect(newValue: string, oldValue: string) {
    // 将用户的选择持久化存储到 Local Storage
    localStorage.setItem(PROJECT_PATH_SELECT, newValue);
  }

  @Watch('manifestSelect')
  private watchManifestSelect(newValue: string, oldValue: string) {
    // 将用户的选择持久化存储到 Local Storage
    localStorage.setItem(MANIFEST_REVISION_SELECT, newValue);
  }

  private mounted() {
    const self: any = this;
    // console.log('page mounted.');
    // 从 Local Storage 中读取用户上次的选择
    const projectSelect = localStorage.getItem(PROJECT_PATH_SELECT);
    if (projectSelect === SELECT_PROJECT_FLAG || projectSelect === SELECT_PATH_FLAG) {
      this.projectSelect = projectSelect
    }
    const manifestSelect = localStorage.getItem(MANIFEST_REVISION_SELECT);
    if (manifestSelect === SELECT_MANIFEST_FLAG || manifestSelect === SELECT_REVISION_FLAG) {
      this.manifestSelect = manifestSelect
    }
    // project 自动完成列表
    self.$axios.get('static/projects.list').then((res: AxiosResponse<string>) => {
      const projects = res.data.split('\n');
      this.projects = projects.map(project => {
        return {
          value: project
        }
      });
    });
    // path 自动完成列表
    self.$axios.get('static/paths.list').then((res: AxiosResponse<string>) => {
      const paths = res.data.split('\n');
      this.paths = paths.map(path => {
        return {
          value: path
        }
      });
    });
    // manifest 自动完成列表
    self.$axios.get('static/manifests.list').then((res: AxiosResponse<string>) => {
      const manifests = res.data.split('\n');
      this.manifests = manifests.map(manifest => {
        return {
          value: manifest
        }
      });
    });
    // revision 自动完成列表
    self.$axios.get('static/revisions.list').then((res: AxiosResponse<string>) => {
      const revisions = res.data.split('\n');
      this.revisions = revisions.map(revision => {
        return {
          value: revision
        }
      });
    });
    // 数据更新时间等信息
    self.$axios.get('static/data_info.json').then((res: AxiosResponse<DataInfo>) => {
      const data = res.data;
      this.dataUpdateTime = data.update_time;
      this.manifestFilesNum = data.manifest_files_num;
      this.projectsNum = data.projects_num;
      this.revisionsNum = data.revisions_num;
    });
    // 全局添加按键监听
    document.onkeydown = (event: KeyboardEvent) => {
      return this.keyCheck(event)
    };
    // 解析 URL 参数
    const query = this.$route.query;
    // console.log('query', query);
    const project = query.project;
    const path = query.path;
    const manifest = query.manifest;
    const revision = query.revision;
    console.log('project:', project, 'path:', path, 'manifest:', manifest, 'revision:', revision);
    if (project) {
      this.projectSelect = SELECT_PROJECT_FLAG;
      if (Array.isArray(project)) {
        this.project = project[0]!!
      } else {
        this.project = project
      }
    }
    if (path) {
      this.projectSelect = SELECT_PATH_FLAG;
      if (Array.isArray(path)) {
        this.project = path[0]!!
      } else {
        this.project = path
      }
    }
    if (manifest) {
      this.manifestSelect = SELECT_MANIFEST_FLAG;
      if (Array.isArray(manifest)) {
        this.manifest = manifest[0]!!
      } else {
        this.manifest = manifest
      }
    }
    if (revision) {
      this.manifestSelect = SELECT_REVISION_FLAG;
      if (Array.isArray(revision)) {
        this.manifest = revision[0]!!
      } else {
        this.manifest = revision
      }
    }
    // 如果 project or path or manifest 不为空，开始搜索
    if (this.project || (this.manifest && this.manifestSelect === SELECT_MANIFEST_FLAG)) {
      this.search()
    }
  }

  private keyCheck(event: KeyboardEvent) {
    // 键盘按键监听处理
    // console.log(event);
    const inputProject = this.$refs.input_project as Autocomplete;
    const inputManifest = this.$refs.input_manifest as Autocomplete;
    if (this.helpDialogVisible) {
      const key = event.key.toLowerCase();
      if (key !== 'shift' && key !== 'control' && key !== 'alt' && key !== 'contextmenu' &&
        key !== "capslock" && key !== "numlock" && key !== "pause") {
        // 隐藏网站帮助
        this.helpDialogVisible = false;
        return false
      }
    } else {
      // Project/Path 输入框
      const projectInput = inputProject.$el.querySelectorAll('input')[1];
      // Manifest/Revision 输入框
      const manifestInput = inputManifest.$el.querySelectorAll('input')[1];

      if (event.key.toLowerCase() === 'enter') {
        this.search();
        // 让输入框失去焦点
        projectInput.blur();
        manifestInput.blur();
        return false
      } else if (event.key.toLowerCase() === 'p') {
        // Project 输入框获取焦点
        if (document.activeElement !== projectInput && document.activeElement !== manifestInput) {
          inputProject.focus();
          // 阻止 按键事件继续传递
          return false
        }
      } else if (event.key.toLowerCase() === 'm') {
        // Manifest 输入框获取焦点
        if (document.activeElement !== projectInput && document.activeElement !== manifestInput) {
          inputManifest.focus();
          // 阻止 按键事件继续传递
          return false
        }
      } else if (event.key === '?') {
        if (document.activeElement !== projectInput && document.activeElement !== manifestInput) {
          // 显示网站帮助
          this.helpDialogVisible = !this.helpDialogVisible;
          return false
        }
      }
    }
    return true
  }

  /**
   * 双击单元格触发事件
   * @param row
   * @param column
   * @param cell
   * @param event
   */
  private cellDoubleClick(row: any, column: any, cell: any, event: any) {
    // console.log(row);
    // console.log(column);
    // console.log(cell);
    // console.log(event);
    if (column.property === 'manifest') {
      // 双击的 manifest
      this.manifest = cell.textContent;
      this.manifestSelect = SELECT_MANIFEST_FLAG;
      this.project = '';
      this.loadDataFromManifest(false)
    } else if (column.property === 'project') {
      // 双击的 project
      this.project = cell.textContent;
      this.projectSelect = SELECT_PROJECT_FLAG;
      this.manifest = '';
      this.loadDataFromProject(false)
    } else if (column.property === 'path') {
      // 双击的 path
      this.project = cell.textContent;
      this.projectSelect = SELECT_PATH_FLAG;
      this.manifest = '';
      this.loadDataFromProject(false)
    }
  }

  /**
   * project/path 输入建议（自动完成）
   * @param queryString 输入的查询字符串
   * @param cb 回调函数
   */
  private queryProject(queryString: string, cb: Function) {
    let projects: Value[] = [];
    if (this.projectSelect === SELECT_PROJECT_FLAG) {
      projects = this.projects;
    } else if (this.projectSelect === SELECT_PATH_FLAG) {
      projects = this.paths;
    }
    const results = queryString ? projects.filter(this.createFilter(queryString)) : projects;
    // 调用 callback 返回建议列表的数据
    cb(results);
  }

  /**
   * manifest/revision 输入建议（自动完成）
   * @param queryString 输入的查询字符串
   * @param cb 回调函数
   */
  private queryManifest(queryString: string, cb: Function) {
    let manifests: Value[] = [];
    if (this.manifestSelect === SELECT_MANIFEST_FLAG) {
      manifests = this.manifests;
    } else if (this.manifestSelect === SELECT_REVISION_FLAG) {
      manifests = this.revisions;
    }
    const results = queryString ? manifests.filter(this.createFilter(queryString)) : manifests;
    // 调用 callback 返回建议列表的数据
    cb(results);
  }

  /**
   * 自动完成列表过滤条件
   * @param queryString 输入的查询字符串
   */
  private createFilter(queryString: string) {
    return (item: Value) => {
      return (item.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
    };
  }

  private handleSelect(item: any) {
    // 点击选中建议项时触发
    // console.log(item);
  }

  /**
   * 根据 manifest file 加载数据
   * @param filterProject 是否过滤 project/path
   */
  private loadDataFromManifest(filterProject: boolean) {
    const self: any = this;
    const manifest = encodeURIComponent(this.manifest);
    console.log('loadDataFromManifest', manifest);
    // 查询字符串（URL query）
    const queryParams = { query: { 'manifest': this.manifest, project: '', path: '' } };
    if (filterProject && this.project) {
      if (this.projectSelect === SELECT_PROJECT_FLAG) {
        queryParams.query.project = this.project;
      } else if (this.projectSelect === SELECT_PATH_FLAG) {
        queryParams.query.path = this.project;
      }
    }
    // 修改 URL query string
    this.$router.replace(queryParams).catch(err => {
      console.log('err', err)
    });
    self.$axios.get(encodeURI('static/manifests/' + manifest)).then((res: AxiosResponse<Data[]>) => {
      // console.log(res.data)
      if (!filterProject || !this.project) {
        this.tableData = res.data;
        if (this.tableData.length === 0) {
          this.$message.error('manifest: ' + this.manifest + ' 不包含 project');
        }
      } else {
        if (this.projectSelect === SELECT_PROJECT_FLAG) {
          this.tableData = res.data.filter((val) => {
            return val.project === this.project
          })
        } else {
          this.tableData = res.data.filter((val) => {
            return val.path === this.project
          })
        }
        if (this.tableData.length === 0) {
          this.$message.error('没有匹配项： manifest: ' + this.manifest + ' AND ' + this.projectSelect + ': ' + this.project);
        }
      }
      this.resetRevisionFilters()
    }).catch((error: AxiosError) => {
      console.log(error);
      this.tableData = [];
      this.$message.error('未找到 Manifest 文件：' + this.manifest);
    });
  }

  /**
   * 根据 project name or path 加载数据
   * @param filterRevision 是否过滤 revision
   */
  private loadDataFromProject(filterRevision: boolean) {
    const self: any = this;
    const project = encodeURIComponent(this.project);
    console.log('loadDataFromProject', project);
    let url: string;
    // 查询字符串（URL query）
    const queryParams = { query: { project: '', path: '', revision: '' } };
    if (this.projectSelect === SELECT_PROJECT_FLAG) {
      queryParams.query.project = this.project;
      url = 'static/projects/' + project
    } else {
      queryParams.query.path = this.project;
      url = 'static/paths/' + project
    }
    if (filterRevision && this.manifest) {
      queryParams.query.revision = this.manifest;
    }
    // 修改 URL query string
    this.$router.replace(queryParams).catch(err => {
      console.log('err', err)
    });
    self.$axios.get(encodeURI(url)).then((res: AxiosResponse<Data[]>) => {
      // console.log(res.data)
      if (!filterRevision || !this.manifest) {
        this.tableData = res.data;
      } else {
        this.tableData = res.data.filter((val) => {
          return val.revision === this.manifest
        });
        if (this.tableData.length === 0) {
          this.$message.error('没有匹配项： ' + this.projectSelect + ': ' + this.project + ' AND revision: ' + this.manifest);
        }
      }
      this.resetRevisionFilters()
    }).catch((error: AxiosError) => {
      console.log(error);
      this.tableData = [];
      if (this.projectSelect === SELECT_PROJECT_FLAG) {
        this.$message.error('未找到 Project：' + this.project);
      } else {
        this.$message.error('未找到 Path：' + this.project);
      }
    });
  }

  /**
   * 执行搜索
   */
  private search() {
    this.loading = true;
    this.project = this.project.trim();
    this.manifest = this.manifest.trim();
    if (!this.project && (!this.manifest || this.manifestSelect === SELECT_REVISION_FLAG)) {
      this.$message.error('Project/Path 和 Manifest 需要至少填写一项');
    } else if (!this.project && this.manifestSelect === SELECT_MANIFEST_FLAG) {
      // manifest 有值
      this.loadDataFromManifest(false)
    } else if (!this.manifest) {
      // project 有值
      this.loadDataFromProject(false)
    } else {
      // project 和 manifest 都有值
      if (this.manifestSelect === SELECT_MANIFEST_FLAG) {
        this.loadDataFromManifest(true)
      } else if (this.manifestSelect === SELECT_REVISION_FLAG) {
        this.loadDataFromProject(true)
      }
    }
    this.loading = false;
  }

  /**
   * 重置 revision 过滤列表
   */
  private resetRevisionFilters() {
    // 清除过滤
    (this.$refs.main_table as Table).clearFilter();
    this.revisionFilters = [];
    const revisionSet = new Set<string>();
    this.tableData.forEach((value) => {
      revisionSet.add(value.revision)
    });
    revisionSet.forEach((value: string) => {
      const obj: FilterItem = {
        text: value,
        value: value
      };
      this.revisionFilters.push(obj)
    });
  }

  /**
   * revision 过滤方法
   * @param value
   * @param row
   * @param column
   * @returns {boolean}
   */
  private filterRevision(value: any, row: any, column: any) {
    const property = column['property'];
    return row[property] === value;
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="stylus">
#main-container {
  margin: 0 20px 0 20px;

  .el-header {
    padding: 0;
  }

  .inline-input {
    width: 100%;
    margin-right: 10px;
  }

  .inline-button {
    width: 100%;
  }

  .el-select .el-input {
    width: 130px;
  }

  .el-table td {
    padding: 8px 0;
  }

  .el-table th {
    padding: 4px 0;
  }

  .el-footer {
    display: flex;
    flex-direction: column;
    -webkit-align-items: center;
    align-items: center;
    -webkit-justify-content: center;
    justify-content: center;
  }

  #footer {
    font-size: 12px;
    margin: 0;
    padding: 0;
    color: #afb4bf;
  }
}
</style>
