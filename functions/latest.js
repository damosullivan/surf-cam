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
      console.log(data);
      let latest = data.Contents[0];
      return {
        statusCode: 200,
        body: JSON.stringify(latest),
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
