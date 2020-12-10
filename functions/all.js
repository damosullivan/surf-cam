const S3 = require("aws-sdk/clients/s3");
const { BACKBLAZE_KEY_ID, BACKBLAZE_APPLICATION_KEY } = process.env;

const s3 = new S3({
  endpoint: "https://s3.us-west-000.backblazeb2.com",
  accessKeyId: BACKBLAZE_KEY_ID,
  secretAccessKey: BACKBLAZE_APPLICATION_KEY,
});

exports.handler = async (event, context) => {
  var params = {
    Bucket: "farranahown-com",
  };

  return s3ListObject(s3, params)
    .then((data) => {
      let keys = data.Contents.map((content) => content.Key);

      // {
      //   "Key": "1607458428.jpeg",
      //   "LastModified": "2020-12-08T20:13:49.000Z",
      //   "ETag": "\"e7f76d892c8240e59501ef830c82fa55\"",
      //   "Size": 76633,
      //   "StorageClass": "STANDARD"
      // }

      return {
        statusCode: 200,
        body: JSON.stringify(keys),
      };
    })
    .catch((err) => {
      return {
        statusCode: 500,
        body: err.toString(),
      };
    });
};

// Promises FTW
const s3ListObject = async (s3, params) => {
  return new Promise((resolve, reject) => {
    s3.listObjectsV2(params, (err, data) => {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
};
