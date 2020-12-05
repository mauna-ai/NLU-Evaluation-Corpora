const _ = require("lodash");

const { entityClassToHolmesMapping: mapping } = require("./constants");
const { remove, rename } = require("./misc");
const { paraphrase } = require("./nlu");

const paraphrasify = async s => {
  const ents = _.map(s.entities, "text");
  const inputs = await paraphrase(s.text);
  inputs.push(s.text);

  return {
    ...s,
    inputs: inputs.filter(s => _.every(ents, e => s.includes(e)))
  };
};

const templatify = s => {
  let match = s.text;

  for (let {entity, text} of s.entities) {
    const holmes = mapping[entity];
    match = _.replace(match, text, holmes);
  }

  return {
    ...s,
    match
  };
};

const collectSimilar = n => (s, idx, all) => {
  const copy = _.cloneDeep(s);

  const similar = _.groupBy(all, "intent")[copy.intent];
  const similarTemplates = _(similar)
    .shuffle()
    .filter(t => t.text !== copy.text)
    .take(n-1)
    .map(templatify)
    .map("match")
    .value();

  copy.templates = copy.templates || [copy.match];
  copy.templates.push(...similarTemplates);

  return copy;
};

const collectOthers = n => (s, idx, all) => {
  const copy = _.cloneDeep(s);

  const others1 = _(all)
    .groupBy("intent");

  const others = _(others1)
    .omit(copy.intent)
    .values()
    .flatten()
    .value();

  const otherTemplates = _(others)
    .shuffle()
    .take(n)
    .map(templatify)
    .map("match")
    .uniq()
    .value();

  copy.templates.push(...otherTemplates);

  return copy;
};

const cleanup = s => {
  const copy = _.cloneDeep(s);

  remove(copy, "intent");
  remove(copy, "text");

  copy.entities.forEach(
    ent => {
      rename(ent, "entity", "entityType");
      remove(ent, "start");
      remove(ent, "stop");
      ent.holmesIdentifier = mapping[ent.entityType];
    });

  return copy;
};

module.exports = [
  _.memoize(paraphrasify),
  templatify,
  collectSimilar(2),
  collectOthers(4),
  cleanup
].reverse();
