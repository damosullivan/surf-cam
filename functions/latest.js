const S3 = require("aws-sdk/clients/s3");
const { AWS_ACCESS_KEY_ID_RW, AWS_SECRET_ACCESS_KEY_RW } = process.env;

const s3 = new S3({
  accessKeyId: AWS_ACCESS_KEY_ID_RW,
  secretAccessKey: AWS_SECRET_ACCESS_KEY_RW,
});

exports.handler = async (event, context) => {
  var params = {
    Bucket: "farranahown",
  };

  return s3ListObject(s3, params)
    .then((data) => {
      console.log(data);
      let latest = data.Contents[0];
      return {
        statusCode: 200,
        body: latest,
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
