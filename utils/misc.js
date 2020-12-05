const contains = (str, substr) => !!~str.indexOf(substr);

const remove = (obj, key) => {
  delete obj[key];
  return obj;
};

const rename = (obj, key, newKey) => {
  obj[newKey] = obj[key];
  remove(obj, key);

  return obj;
};

module.exports = {
  contains,
  remove,
  rename
};
