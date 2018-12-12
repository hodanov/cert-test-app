import React from 'react';
import ReactDOM from 'react-dom';
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUpload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
library.add(faUpload)

class Form extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFileName: {
        'crt': null,
        'incrt': null,
        'key': null,
      },
      certificatesTest: false,

    };
  }

  handleChange(fileType, e) {// 選択ボタンの押下をトリガーに、選択されたファイル名を取得
    if (e.target.files.length == 1) {
      var fileName = e.target.files[0].name;
      const files = this.state.selectedFileName;
      files[fileType] = fileName;
      this.setState({
        selectedFileName: files,
      });
    }
  }

  renderSelectBox(fileType) {// ファイル選択ボタンのレンダリング
    if (fileType == "crt") {
      var acceptFileType = '.cer, .crt'
      var labelName = 'サーバー証明書'
    }
    else if (fileType == "incrt"){
      var acceptFileType = '.cer, .crt'
      var labelName = '中間証明書'
    }
    else if (fileType == "key") {
      var acceptFileType = '.key'
      var labelName = '秘密鍵'
    }
    return (
      <div className="column is-4 file has-name is-boxed" key={fileType}>
        <label className="file-label">
          <input id={fileType} className="file-input" type="file" name={fileType} accept={acceptFileType} onChange={(e) => this.handleChange(fileType, e)} />
          <p className="file-cta">
            <span className="file-icon">
              <FontAwesomeIcon icon="upload" />
            </span>
            <span className="file-label">
              {labelName}
            </span>
          </p>
          <p id={fileType + "-name"} className="file-name">
            <span>{this.state.selectedFileName[fileType]}</span>
          </p>
        </label>
      </div>
    );
  }

  check() {// 証明書ファイルの選択判定
    var checkCrt = this.state.selectedFileName['crt'];
    var checkIncrt = this.state.selectedFileName['incrt'];
    var checkKey = this.state.selectedFileName['key']
    if (checkCrt == null || checkIncrt == null || checkKey == null) {
      return false;
    }
    else {
      return true;
    }
  }

  renderStartBtn() {// Startボタンのレンダリング
    if (this.check() == true) {// 証明書ファイルが選択されている場合
      return (
        <button type="submit" className="button is-large is-fullwidth is-primary" key="uploadBtn">テスト実行</button>
      );
    }
    else {// 証明書ファイルが選択されていない場合、disabled属性を付与したボタンを出力
      return (
        <button type="submit" className="button is-large is-fullwidth is-primary" key="uploadBtn" disabled>テスト実行</button>
      );
    }
  }

  render() {// ボタンコンポーネントのレンダリング
    return ([
      <div className="columns" key="selectBtn">
        {this.renderSelectBox("crt")}
        {this.renderSelectBox("incrt")}
        {this.renderSelectBox("key")}
      </div>,
      this.renderStartBtn(),
    ]);
  }
}

ReactDOM.render(
  <Form />,
  document.getElementById('choose-file-forms')
);
