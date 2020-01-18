import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class count {
    public static class FilterBudMapper
    extends Mapper < Object, Text, Text, IntWritable > {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException,
        InterruptedException {
            // Turn value into a string and split it at the commas
            String s = value.toString();
            String[] split = s.split(",");

            // Make sure that the entry has a bar, beer, and price
            if (split.length == 3) {
                String bar = split[0];
                String beer = split[1];
                int price = Integer.parseInt(split[2]);

                // Check if the first three characters of the beer = "Bud"
                if (beer.length() >= 3 && beer.substring(0, 3).equals("Bud")) {
                    context.write(new Text(bar), new IntWritable(price));
                }
            }
        }
    }

    public static class CountBeersReducer
    extends Reducer < Text, IntWritable, Text, IntWritable > {
        private IntWritable result = new IntWritable();
        public void reduce(Text key, Iterable < IntWritable > values,
            Context context
        ) throws IOException,
        InterruptedException {
            int count = 0;
            for (IntWritable val: values) {
                int price = val.get();
                if (price > 5) {
                    return; // Do not output this bar if it has a Bud price > 5.
                }
                count++;
            }
            result.set(count);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
        if (otherArgs.length != 2) {
            System.err.println("Usage: count <in> <out>");
            System.exit(2);
        }
        Job job = Job.getInstance(conf, "count");
        job.setJarByClass(count.class);
        job.setMapperClass(FilterBudMapper.class);
        job.setReducerClass(CountBeersReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job,
            new Path(otherArgs[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
