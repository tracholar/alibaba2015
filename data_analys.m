%data = textread('data.train.csv','%f','delimiter',',','headerlines',1);
%data = reshape(data(:),156, 32038812/156);
%data = data';
X=data(:,3:end-1);Y=data(:,end);
X = X(:, [1:16 18:62 64:end]);
X_mu = mean(X);
X_std = std(X);
X_new = bsxfun(@rdivide, bsxfun(@minus, X,X_mu), X_std);

figure;
samples = rand(length(Y),1)<.1;
scatter(X_new((Y==0) & samples, 60), X_new((Y==0)&samples, 2),'r.');
hold on;
scatter(X_new(Y==1, 60), X_new(Y==1, 2),'k+');
hold off;

m = cov(X_new);

[U D V] = svd(m);
n = 100;
sum(diag(D(1:n,1:n))) / sum(diag(D))
X_r = bsxfun(@minus, X_new , mean(X_new)) * V(:,1:n);

figure;
samples = rand(length(Y),1)<.1;
scatter(X_r((Y==0) & samples, 1), X_r((Y==0)&samples, 2),'r.');
hold on;
scatter(X_r(Y==1, 1), X_r(Y==1, 2),'k+');
